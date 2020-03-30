import unittest

from api.simplex import SimplexMethodSolver


class SimplexTest(unittest.TestCase):

    def test_right_simlex_resolver_work_1(self):
        func = "3x1 + 2x2 + x3"
        method = False
        bounds = [
            "x2 + x3 >= 4",
            "2x1 + x2 + 2x3 >= 6",
            "2x1 - x2 + 2x3 >= 2"
        ]

        result = SimplexMethodSolver.find_solution(func, bounds, method)
        self.assertEqual([0.0, 0.0, 4.0], result)

    def test_right_simlex_resolver_work_2(self):
        func = "2x1 + 3x2 - x4"
        method = True
        bounds = [
            "2x1 - x2 - 2x4 + x5 = 16",
            "3x1 + 2x2 + x3 - 3x4 = 18",
            "-x1 + 3x2 + 4x4 + x6 = 24"
        ]

        result = SimplexMethodSolver.find_solution(func, bounds, method)
        print(result)
        self.assertEqual([0.54545455, 8.1818182, 0.0, 0.0, 23.090909, 0.0], result)
