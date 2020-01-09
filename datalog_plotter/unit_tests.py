import unittest
from pathlib import Path
import numpy as np
from datalog_plotter import *

file_directory="test_data\\Test Dataset_2020101_111111"
test_data_file=Path(file_directory) / "data"/"dut0.dat"

class Tests(unittest.TestCase):
    def test_folder_import(self):
        # assert that passing a valid path from the command line returns that path as a path object

        self.assertEqual(get_test_directory(file_directory) , Path(file_directory))

        # passing an invalid path should raise an exception

        with self.assertRaises(ValueError):
            get_test_directory("Cat")

        try:
            get_test_directory()
        except:
            self.fail("passing no arguments to test directory raised an exception")

    def test_data_import(self):
        headers,data_dict=import_data_from_file(test_data_file)
        # assert that we generated data for every key
        self.assertEqual(headers,list(data_dict.keys()))
        # assert that for every data field in header the sum is 100*j where J is the column
        for j,header in enumerate(headers[1:]):
            self.assertEqual(100*(j+1),np.sum(data_dict[header]))

    def test_RPN_with_values(self):
        calc=RPNWithData()  # make a new calculator
        self.assertEqual(calc.calculate("7 8 ADD"),15)  # assert that 7+8=15
        self.assertAlmostEqual(calc.calculate("8.5 7.8 SUB"), -0.7)  # assert that subtraction and float math works
        self.assertEqual(calc.calculate("7 8 MUL"), 56)  # assert that 7*8=56
        self.assertEqual(calc.calculate("8 64 DIV"), 8)  # assert that 64/8=8
        self.assertEqual(calc.calculate("64 SQR"),8)    # squareroot

    def test_RPN_with_data(self):
        calc = RPNWithData()  # make a new calculator
        _, data_dict = import_data_from_file(test_data_file)
        calc.load_data(data_dict)
        self.assertEqual(np.sum(calc.calculate("$SltACh1 8 MUL")), 800)  # multiply by a constant
        self.assertEqual(np.sum(calc.calculate("2 $SltBCh1 DIV")), 100)  # divide by a constant
        self.assertEqual(np.sum(calc.calculate("$SltACh1 8 ADD")), 900)  # add a constant
        self.assertEqual(np.sum(calc.calculate("8 $SltDCh2 SUB")), 0)  # subtract a constant
        self.assertAlmostEqual(calc.calculate("$SltACh1 $SltDCh2 MUL")[0], 8)  # Multiply two arrays
        self.assertAlmostEqual(calc.calculate("$SltACh2 $SltDCh2 SUB")[0], 4)  # Divide two arrays
        self.assertAlmostEqual(calc.calculate("$SltACh1 $SltDCh2 ADD")[0], 9)  # Add two arrays
        self.assertAlmostEqual(calc.calculate("$SltACh1 $SltDCh2 SUB")[0], 7)  # Subtract two arrays

    def test_RPN_complex_math(self):
        calc = RPNWithData() # make a new calculator
        self.assertEqual(calc.calculate("4 8 8 ADD DIV SQR"),2)

