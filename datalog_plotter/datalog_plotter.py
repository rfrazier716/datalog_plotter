from pathlib import Path
import numpy as np
import csv
import itertools
import json


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
                    self._stack.append(self._data[command[1:]])  # append data to the stack
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


def get_test_directory(*args):
    if args:
        # if the directory was provides as a command line argument do not have user select one
        file_path = Path(args[0])
    else:
        # if we didn't provide a path make a dialog box to select it
        import tkinter as tk  # import tkinter
        from tkinter import filedialog  # import the file dialog

        root = tk.Tk()
        root.withdraw()  # make a root window but hide it

        file_path = Path(filedialog.askdirectory(title="Select Test Folder"))

    # verify file is a directory
    if not file_path.is_dir():
        raise ValueError("the input {} is not a valid directory".format(file_path))
    if not (file_path / "data").is_dir():
        # verify there is a data subdirectory in the test folder
        raise ValueError(" Did not find a data subdirectory in test folder")

    return file_path


def generate_plots(data_folder):
    for file_path in data_folder.glob("*.dat"):
        data = np.genfromtxt(file_path, dtype="float", delimiter='\t', names=True)


def import_data_from_file(file_path):
    with open(file_path) as file:
        reader = csv.reader(file, delimiter='\t')  # make a csv reader object
        headers = [header for header in next(reader) if header]  # extract headers and only return nonempty strings
        headers[0] = headers[0][1:]  # get rid of the comment character on the first header
        next(reader)  # consume the next line which is a comment divider
        data = np.array(list(reader)).astype(float)  # import data
        # convert data to a dict of columns
        data_dict = {field_name: data for field_name, data in zip(headers, data.T)}
        return headers, data_dict


def main():
    # get path of folder to import data
    parent_path = get_test_directory()
    data_folder = parent_path / "data"
    generate_plots(data_folder)
    # get path of folder to import data


if __name__ == "__main__":
    main()
