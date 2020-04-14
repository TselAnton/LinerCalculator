import unittest

from api.Simplex import SimplexMethodSolver


class SimplexTest(unittest.TestCase):

    def test_right_simplex_resolver_work_1(self):
        func = "3x1 + 2x2 + x3"
        method = False
        bounds = [
            "x2 + x3 >= 4",
            "2x1 + x2 + 2x3 >= 6",
            "2x1 - x2 + 2x3 >= 2"
        ]

        result, values = SimplexMethodSolver.find_solution(func, bounds, method)
        self.assertEqual([0.0, 0.0, 4.0], values)

    def test_right_simplex_resolver_work_2(self):
        func = "11x1 + 5x2 + 4x3"
        method = True
        bounds = [
            "3x1 + 2x2 + 8x3 >= 11",
            "2x1 + x3 <= 5",
            "3x1 + 3x2 + x3 <= 13",
            "x1>=3.0"
        ]

        result, values = SimplexMethodSolver.find_solution(func, bounds, method)
        self.assertIsNone(result)
