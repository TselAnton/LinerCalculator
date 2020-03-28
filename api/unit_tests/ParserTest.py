import unittest

from api.parser import Parser, ParserException


class ParserTest(unittest.TestCase):

    def test_main_function_with_one_cof(self):
        self.check_parser_with_main_function("1*x1", 1, [1], None)
        self.check_parser_with_main_function("-1*x1", 1, [-1], None)
        self.check_parser_with_main_function("-x1", 1, [-1], None)
        self.check_parser_with_main_function("+x1", 1, [1], None)

    def test_main_function_with_many_cof(self):
        self.check_parser_with_main_function("1*x1+2*x2", 2, [1, 2], None)
        self.check_parser_with_main_function("1x1+2x2", 2, [1, 2], None)
        self.check_parser_with_main_function("x1-2x2", 2, [1, -2], None)
        self.check_parser_with_main_function("x1-x2", 2, [1, -1], None)
        self.check_parser_with_main_function("-x1-2x2-3x3", 3, [-1, -2, -3], None)
        self.check_parser_with_main_function("-x1-2x2-3x3+100", 3, [-1, -2, -3], 100)

    def test_bound_function(self):
        self.check_parser_with_borders("1*x1+2*x2+3*x3 <= 100", 3, [1, 2, 3], None, [0, 0, 0], 100, "<=")
        self.check_parser_with_borders("-1*x1-2*x2-3*x3 >= -100", 3, [-1, -2, -3], None, [0, 0, 0], -100, ">=")
        self.check_parser_with_borders("-x1-x2-x3 = -x1-x2-x3", 3, [-1, -1, -1], None, [-1, -1, -1], None, "=")
        self.check_parser_with_borders("-x1 < -3", 1, [-1], None, [0], -3, "<")
        self.check_parser_with_borders("-3 > -x1", 1, [0], -3, [-1], None, ">")
        self.check_parser_with_borders("-3>  =-x1", 1, [0], -3, [-1], None, ">=")

    def test_bound_BCE_Exception(self):
        with self.assertRaises(ParserException):
            Parser.parse_function_with_borders("-x1 => -3", 1)

    def test_get_US_Exception(self):
        with self.assertRaises(ParserException):
            Parser.parse_alone_function("1+x1", 1)

    def test_get_UF_Exception(self):
        with self.assertRaises(ParserException):
            Parser.parse_alone_function("1*x1+", 1)

    def test_get_UC_Exception(self):
        with self.assertRaises(ParserException):
            Parser.parse_alone_function("k1+x1", 1)

    def check_parser_with_main_function(self, str_fun, num_of_cof, expected_array_cof, expected_free_cof):
        cof_array, free_cof = Parser.parse_alone_function(str_fun, num_of_cof)
        self.assertEqual(expected_free_cof, free_cof)
        self.assertEqual(expected_array_cof, cof_array)

    def check_parser_with_borders(self, str_fun, num_of_cof, exp_left_cof,
                                  exp_left_free, exp_right_cof, exp_right_free, exp_border):
        cof_array, free_array, border = Parser.parse_function_with_borders(str_fun, num_of_cof)
        self.assertEqual(exp_left_cof, cof_array[0])
        self.assertEqual(exp_left_free, free_array[0])
        self.assertEqual(exp_right_cof, cof_array[1])
        self.assertEqual(exp_right_free, free_array[1])
        self.assertEqual(exp_border, border)
