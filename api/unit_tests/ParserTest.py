import unittest

from api.parser import Parser, ParserException


class ParserTest(unittest.TestCase):

    def test_main_function_with_one_cof(self):
        self.check_parser("1*x1", 1, [1], None)
        self.check_parser("-1*x1", 1, [-1], None)
        self.check_parser("-x1", 1, [-1], None)
        self.check_parser("+x1", 1, [1], None)

    def test_main_function_with_many_coef(self):
        self.check_parser("1*x1+2*x2", 2, [1, 2], None)
        self.check_parser("1x1+2x2", 2, [1, 2], None)
        self.check_parser("x1-2x2", 2, [1, -2], None)
        self.check_parser("-x1-2x2-3x3", 3, [-1, -2, -3], None)
        self.check_parser("-x1-2x2-3x3+100", 3, [-1, -2, -3], 100)

    def test_get_US_Exception(self):
        with self.assertRaises(ParserException) as exc:
            Parser.parse_alone_function("1+x1", 1)

    def test_get_UF_Exception(self):
        with self.assertRaises(ParserException) as exc:
            Parser.parse_alone_function("1*x1+", 1)

    def test_get_UC_Exception(self):
        with self.assertRaises(ParserException) as exc:
            Parser.parse_alone_function("k1+x1", 1)

    def check_parser(self, str_fun, num_of_cof, expected_array_cof, expected_free_cof):
        cof_array, free_cof = Parser.parse_alone_function(str_fun, num_of_cof)
        self.assertEqual(expected_free_cof, free_cof)
        self.assertEqual(expected_array_cof, cof_array)
