import sys
from pathlib import Path
import numpy as np
import csv
import json
import math
from matplotlib import pyplot as plt
import terminalio

version_major = 1
version_minor = 1


class PlotParameter():
    def __init__(self, name, subplot, y_label, normalize, decimation, rpn_calculation):
        self.name = name
        self.subplot_value = subplot
        self.y_label = y_label
        self.normalize = normalize
        self.decimation = decimation
        self.rpn_calculation = rpn_calculation


class RPNWithData():
    # an RPN Calculator that has a named data fields loaded in which can be addressed

    def __init__(self, data=None):
        self.reset()
        self._data = data

        # dict of operations the calculator can perform
        self._operations_dict = {
            "ADD": self._add,
            "SUB": self._sub,
            "MUL": self._multiply,
            "DIV": self._divide,
            "SQR": self._squareroot
        }

    def reset(self):
        self._stack = []  # stack is a list of strings that holds

    def load_data(self, data):
        self._data = data

    def calculate(self, calculation_string):
        for command in calculation_string.split():
            # if a command is a variable name or quantity, push it onto the stack
            if command in self._operations_dict.keys():
                # if command is operator, execute operation
                self._operations_dict[command]()
            else:
                # variable names must be prefixed by a $ or else it will try to parse things as a number
                if command[0] == "$":
                    self._stack.append(self._data.get(command[1:],
                                                      0))  # append data to the stack, if data field doesn't exist write a zero
                else:
                    self._stack.append(float(command))  # turn the command into a number and push onto stack
        # at the end of the calculation, return the furthest  value on the stack which is the response
        return self._stack[-1]

    def _add(self):
        # consume two values from the stack, add them, and push the result onto the stack
        a = self._stack.pop(-1)
        b = self._stack.pop(-1)
        res = np.add(a, b)
        self._stack.append(res)

    def _sub(self):
        # consume two values from the stack, subtract them, and push the result onto the stack
        a = self._stack.pop(-1)
        b = self._stack.pop(-1)
        res = np.subtract(a, b)
        self._stack.append(res)

    def _multiply(self):
        # consume two values from the stack, multiply them, and push the result onto the stack
        a = self._stack.pop(-1)
        b = self._stack.pop(-1)
        res = np.multiply(a, b)
        self._stack.append(res)

    def _divide(self):
        # consume two values from the stack, divide them, and push the result onto the stack
        a = self._stack.pop(-1)
        b = self._stack.pop(-1)
        res = np.divide(a, b)
        self._stack.append(res)

    def _squareroot(self):
        # consume a single stack value, take the squareroot, and push back onto the stack
        a = self._stack.pop(-1)
        res = np.sqrt(a)
        self._stack.append(res)


def decimate_data(array, decimation):
    # decimates the array and returns the decimated data
    array = array[0:round(decimation * math.floor(array.size / decimation))]
    dec_array = np.mean(array.reshape((round(array.size / decimation), decimation)), axis=1)
    return dec_array


def get_test_directory(*args):
    if args:
        # if the directory was provides as a command line argument do not have user select one
        file_path = Path(args[0])
    else:
        print("no directory provided, please select path to test file")
        # if we didn't provide a path make a dialog box to select it
        import tkinter as tk  # import tkinter
        from tkinter import filedialog  # import the file dialog

        root = tk.Tk()
        root.withdraw()  # make a root window but hide it

        file_path = Path(filedialog.askdirectory(title="Select Test Folder"))
        root.destroy()

    # verify file is a directory
    if not file_path.is_dir():
        raise ValueError("the input {} is not a valid directory".format(file_path))
    if not (file_path / "data").is_dir():
        # verify there is a data subdirectory in the test folder
        raise ValueError(" Did not find a data subdirectory in test folder")

    return file_path


def verbose_function_call(function, args, comment=""):
    print(comment + "... ", end="")
    return_value = function(*args)
    print("Success!")
    return return_value


def import_plot_settings(file_path):
    # returns a list of plot parameter objects who's settings are stored in a json file
    json_data = None
    with open(file_path) as file:
        json_data = json.load(file)  # load the file into a dict
    return [PlotParameter(plot["name"], plot["subplot"], plot["y_label"], plot["normalize"], plot["decimation"],
                          plot["function"])
            for plot in json_data["plots"]]


def generate_plots(data_folder, plot_settings_path):
    # import plot settings from JSON file
    plot_settings = verbose_function_call(import_plot_settings, [plot_settings_path], "Importing Plot Settings")
    files = list(data_folder.glob("*.dat"))  # list of test files
    print("found {} data file(s) in test folder".format(len(files)))

    for fig_num, file_path in enumerate(files):
        # for every file import data
        print("\nProcessing {}".format(file_path.name))
        _, data_dict = verbose_function_call(import_data_from_file, [file_path], "Importing Data")
        calc = RPNWithData(data_dict)  # make an RPN calculator for this dataset

        fig = plt.figure(fig_num)  # set the figure
        fig.suptitle(file_path.stem, fontsize=16)
        time_arr = (data_dict["Epoch Time"] - data_dict["Epoch Time"][
            0]) / 60  # convert time from seconds to minutes from st
        subplots = {}  # dict of existing subplots
        for fn_num, plot_function in enumerate(plot_settings):
            print("Generating function {}. equation: {}".format(fn_num, plot_function.rpn_calculation))
            # in this figure make the required subplot and plot the data

            # set to the required subplot by either creating one or reusing one
            try:
                ax = subplots[plot_function.subplot_value]  # try to recall the existing subplot
            except KeyError:
                # if it does not exist make a new subplot
                subplots[plot_function.subplot_value] = fig.add_subplot(plot_function.subplot_value)
                ax = subplots[plot_function.subplot_value]

            x_val = decimate_data(time_arr, plot_function.decimation)  # decimate the time field
            # create they y-value of the function
            y_val = decimate_data(calc.calculate(plot_function.rpn_calculation), plot_function.decimation)

            if plot_function.normalize:  # if we want to normalize the data
                y_val = y_val / np.mean(y_val[:10])  # divide by the average of the first 10 datapoints

            # plot the requested data
            ax.plot(x_val, y_val, label=plot_function.name)  # plot the requested function
            ax.set_ylabel(plot_function.y_label)  # set the Y-Axis Label
            ax.set_xlabel("Time (min)")  # set the X-Axis label
            ax.legend()  # update the legend
    plt.legend()
    plt.show()


def import_data_from_file(file_path):
    with open(file_path) as file:
        reader = csv.reader(file, delimiter='\t')  # make a csv reader object
        headers = [header for header in next(reader) if header]  # extract headers and only return nonempty strings
        headers[0] = headers[0][1:]  # get rid of the comment character on the first header
        next(reader)  # consume the next line which is a comment divider
        data = np.array(list(reader))  # import data
        if data[-1, -1] == "":  # if we imported an empty column by accident
            data = data[:, :-1]  # delete that last column
        data = data.astype("float")
        # convert data to a dict of columns
        data_dict = {field_name: data for field_name, data in zip(headers, data.T)}
        return headers, data_dict


def create_processed_data_folder(parent_path):
    processed_data_path = parent_path / "processed"
    if not processed_data_path.exists():
        processed_data_path.mkdir()


def get_plot_settings_file():
    plot_settings_path = Path("plot_settings")
    plot_settings_list = terminalio.get_files_with_extension(plot_settings_path, "json")
    plot_settings_prompt = "Select which plotter parameters to use\n" + "".join(["-" for _ in range(50)])
    plot_settings_selection = terminalio.get_validated_list_selection(plot_settings_list, "> ", plot_settings_prompt,
                                                                      allow_abort=False)
    plot_settings_file = plot_settings_list[plot_settings_selection - 1]  # json file user selects to process data with
    return plot_settings_path / plot_settings_file


def main():
    # get path of folder to import data
    print("ADPD5000 Datalog Plotter V{}.{}".format(version_major, version_minor))
    parent_path = get_test_directory()
    create_processed_data_folder(parent_path)  # make a path if one does not exist to store the processed data
    data_folder = parent_path / "data"
    plot_settings_file = get_plot_settings_file()  # get user selected plot settings
    # TODO: Validate RPN Equations with REGEX and Raise error if not
    generate_plots(data_folder, plot_settings_file)
    print("Program Done, exiting")


if __name__ == "__main__":
    main()
