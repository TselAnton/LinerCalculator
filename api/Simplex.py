from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize, value
from api.Parser import Parser


class SimplexMethodSolver:
    """
    Класс для решения симплекс-методом
    """

    @staticmethod
    def find_solution(function, bounds_array, optimal_model=True):
        """
        Поиск решения симплек-методом
        :param optimal_model: True — MAX / False — MIN
        :param function: Функция
        :param bounds_array: Условия
        :return: Решение симплекс-методом
        """
        max_num_of_func = Parser.find_max_constant(function)
        max_num_of_bounds = Parser.find_max_constant(bounds_array)
        num_of_const = max_num_of_func if max_num_of_func > max_num_of_bounds else max_num_of_bounds

        x = [LpVariable("x" + str(i + 1), lowBound=0) for i in range(num_of_const)]
        problem = LpProblem("0", LpMaximize) if optimal_model else LpProblem("0", LpMinimize)

        # Считаем main функцию
        fun_cof, fun_free = Parser.parse_alone_function(function, num_of_const)
        problem += sum([fun_cof[i] * x[i] for i in range(num_of_const)]) + (0 if fun_cof is None else fun_cof)

        # Считаем коэфициенты
        for bound in bounds_array:
            cof_arr, free_arr, border = Parser.parse_function_with_borders(bound, num_of_const)

            if border == Parser.MORE:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) > \
                    sum([cof_arr[1][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[1] is None else free_arr[1])
            elif border == Parser.MORE_OR_EQUAL:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) >= \
                    sum([cof_arr[1][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[1] is None else free_arr[1])
            elif border == Parser.LESS:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) < \
                    sum([cof_arr[1][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[1] is None else free_arr[1])
            elif border == Parser.LESS_OR_EQUAL:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) <= \
                    sum([cof_arr[1][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[1] is None else free_arr[1])
            elif border == Parser.EQUAL:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) == \
                    sum([cof_arr[1][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[1] is None else free_arr[1])

        problem.solve()
        return [value(problem.objective), [var.varValue for var in problem.variables()]]
