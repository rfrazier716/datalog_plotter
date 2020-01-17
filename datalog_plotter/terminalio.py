'''
Created on Aug 20, 2019

@author: rfrazier
'''
import os
from math import floor, ceil


def comment_padded_word(word, comment_char, total_chars):
    word_len = len(word)
    pre_pad = int(floor(total_chars / 2) - floor(word_len / 2))
    post_pad = int(ceil(total_chars / 2) - ceil(word_len / 2))
    return ''.join([comment_char for j in range(pre_pad)]) + word + ''.join([comment_char for j in range(post_pad)])


def multi_line_input(prompt):
    user_input = ''
    exit_condition = False
    print(prompt + ' (Enter an empty line to exit):')
    while exit_condition != True:
        line = input()
        if (not line.isspace()) and (not line == ''):
            user_input += (line + '\n')
        else:
            exit_condition = True
    return user_input


def console_progress_bar(n, total_items):
    percent_done = 100 * (n + 1) / total_items
    n_equals = floor(percent_done / 5)
    n_spaces = 20 - n_equals
    progress_bar = '[' + ''.join(['=' for j in range(n_equals)]) + '>' + ''.join(
        [" " for j in range(n_spaces)]) + "] " + str(round(percent_done, 0)) + "%"
    return progress_bar


def get_validated_list_selection(items, prompt, header, allow_abort=True):
    valid_input = False
    print(header)
    print_enumerated_list(items)
    if allow_abort:
        print("(-1) Abort Operation")
    selection = ""  # Do you have to do this for the variable scope???
    while not valid_input:
        user_input = input(prompt)
        try:
            selection = int(user_input.split()[0])  # Parse raw input and pull out any numbers that are in the input
        except ValueError:
            selection = -2  # If no numbers detected, set the selection number to an invalid option to trigger an error down the line
        if selection > len(items) or (selection<=0 and selection != -1) or (selection ==-1 and not allow_abort):  # flag invalid user input
            print("[invalid user input]")
        else:
            valid_input = True
    return selection


def yes_no_prompt(header,prompt):
    valid_responses=["y","n","yes","no"] # valid responses to prompt
    valid_input=False # set input to invalid
    print(header + " ([Y]es or [N]o)") # print the prompt
    while not valid_input:
        user_input=input(prompt).lower() # get the selection from the user
        if user_input not in valid_responses:
            print("[invalid user input]")
        else:
            valid_input=True
    # return True or false depending on input
    if user_input[0]=='y':
        return True
    else:
        return False

def get_code_directory():
    return os.path.dirname(os.path.realpath(__file__))


def get_files_with_extension(path, extension):
    files = os.listdir(path)
    config_files = []
    for file in files:
        if file.endswith(extension):
            config_files.append(file)
    return config_files


def print_enumerated_list(string_list):
    for counter, file in enumerate(string_list, 1):
        print("(" + str(counter) + ")" + " " + file)


if __name__ == '__main__':
    pass
