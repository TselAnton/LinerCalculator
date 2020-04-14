from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize, value
from api.Parser import Parser


class SimplexMethodSolver:
    """
    Класс для решения симплекс-методом
    """

    @staticmethod
    def find_solution(function, bounds_array, optimal_model):
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
        fun_cof = Parser.parse_alone_function(function, num_of_const)
        problem += sum([fun_cof[i] * x[i] for i in range(num_of_const)])

        coefficients = []
        arguments = []
        borders = []

        # Считаем коэфициенты
        for bound in bounds_array:
            cof_arr, free_arr, border = Parser.parse_function_with_borders(bound, num_of_const)

            # Запоминаем всю информацию о начальных условиях для дальнейшей проверки
            coefficients.append(cof_arr)
            arguments.append(free_arr)
            borders.append(border)

            if border == Parser.MORE_OR_EQUAL:
                problem += \
                    sum([cof_arr[0][i] * x[i] for i in range(num_of_const)]) + (
                        0 if free_arr[0] is None else free_arr[0]) >= \
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
        variables = [var.varValue for var in problem.variables()]

        if SimplexMethodSolver.__check_to_normal(coefficients, arguments, borders, variables):
            return problem.objective.value(), variables
        return None, []

    @staticmethod
    def __check_to_normal(coefficients, arguments, borders, variables):
        """
        Проверка на возможность решения
        :param coefficients: Массив коэффициентов
        :param arguments: Массив аргументов
        :param borders: Массив условий
        :param variables: Массив значений xn
        :return: True - Возможность существования / False - Не возможность существования
        """
        for i in range(len(variables)):
            left = 0.0
            right = 0.0

            for j in range(len(variables)):
                left += float(coefficients[i][0][j]) * float(variables[j])
            left += float(arguments[i][0]) if not arguments[i][0] is None else 0.0

            for j in range(len(variables)):
                right += float(coefficients[i][1][j]) * float(variables[j])
            right += float(arguments[i][1]) if not arguments[i][1] is None else 0.0

            if abs(left - right) > 0.00001:
                if borders[i] == Parser.MORE_OR_EQUAL:
                    if not left >= right:
                        return False
                elif borders[i] == Parser.LESS_OR_EQUAL:
                    if not left <= right:
                        return False
                else:
                    if not left == right:
                        return False
        return True

