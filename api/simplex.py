from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize
from api.parser import Parser


class SimplexMethodSolver:
    """
    Класс для решения симплекс-методом
    """

    @staticmethod
    def find_solution(num_of_const, optimal_model, function, bounds_array):
        """
        Поиск решения симплек-методом
        :param num_of_const: Количество переменных
        :param optimal_model: True — MAX / False — MIN
        :param function: Функция
        :param bounds_array: Условия
        :return: Решение симплекс-методом
        """
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
        return [var.varValue for var in problem.variables()]

