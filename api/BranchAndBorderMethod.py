import math

from api.Simplex import SimplexMethodSolver as simplex


class BranchAndBorderMethod:
    """
    Метод ветвей и границ
    """

    @staticmethod
    def find_solution(function, bounds_array, optimal_model, max_depth=5, is_multiple_threads=False):
        """
        Поиск решения
        :param max_depth: Максимальное количество слоёв дерева
        :param function: Целевая функция
        :param bounds_array: Ограничения
        :param optimal_model:
        :param is_multiple_threads:
        :return:
        """
        if is_multiple_threads is False:
            return BranchAndBorderMethod \
                .__find_solution_by_single_thread(function, bounds_array, optimal_model, max_depth)
        else:
            # TODO: Многопоточка
            pass

    @staticmethod
    def __find_solution_by_single_thread(function, bounds_array, optimal_model, max_depth):
        """
        Поиск решения в одиночном потоке
        :param function: Целевая функция
        :param bounds_array: Ограничения
        :param optimal_model: Оптимальная модель
        :return: Результат, коэффициенты xn
        """
        tree = Tree(bounds_array, function, optimal_model)  # Создаём древовидную структуру
        tree = BranchAndBorderMethod.__recount_node(tree.root, max_depth)  # Строим дерево

        return BranchAndBorderMethod.find_max(tree) if optimal_model else BranchAndBorderMethod.find_min(tree)

    @staticmethod
    def __recount_node(node, max_depth):
        """
        Пересчитать значение в узле
        :param node: Узел дерева
        :return: Дерево решений
        """
        # Ищем решение
        result, variables = simplex.find_solution(node.get_function(), node.get_bounds(), node.get_model())
        node.set_results(result, variables)  # Задаём текущему узлу получившиеся значения

        float_value, float_num = BranchAndBorderMethod.__get_not_integer_var(variables)  # Находим дробное значение

        print(node.__str__())

        if node.level < max_depth:
            if float_num != -1:
                # Создаём доп ограничения
                left_bound, right_bound = BranchAndBorderMethod.__create_new_bounds(float_value, float_num, node)

                if left_bound is not None:
                    # Создаём левый узел с дополнительным ограничением
                    node.set_left(node.get_bounds(), left_bound, node.get_function(), node.get_model(), node.level + 1)
                    BranchAndBorderMethod.__recount_node(node.get_left(), max_depth)

                if right_bound is not None:
                    # Создаём правый узел с дополнительным ограничением
                    node.set_right(node.get_bounds(), right_bound, node.get_function(), node.get_model(), node.level + 1)
                    BranchAndBorderMethod.__recount_node(node.get_right(), max_depth)

        return node

    @staticmethod
    def __get_not_integer_var(variables):
        """
        Поиск не целого числа из списка всех полученных значений xn
        :param variables: Массив значений xn
        :return: Номер икса, имеющего дробный коэффициент
        """
        for i in range(len(variables)):
            if variables[i] > 0 and not variables[i].is_integer():
                return variables[i], (i + 1)
        return -1, -1

    @staticmethod
    def __is_contains_nulls(variables):
        """
        Содержит ли массив нулевые значения
        :param variables: Массив значений
        :return: True - содержит, False - не содержит
        """
        return sum([1.0 if v == 0 else 0.0 for v in variables]) > 0

    @staticmethod
    def __create_new_bounds(value, num_of_x, node):
        """
        Создание дополнительных ограничений
        :param num_of_x: Номер x
        :param value: Значение коэффициента
        :return: Границы для левого и правого узла дерева
        """
        int_val = math.modf(value)[1]
        left_bound = str("x" + str(num_of_x) + ">=" + str(int_val + 1))
        right_bound = str("x" + str(num_of_x) + "<=" + str(int_val))

        return BranchAndBorderMethod.__get_not_equal_bound(left_bound, node.bound_array), \
               BranchAndBorderMethod.__get_not_equal_bound(right_bound, node.bound_array)

    @staticmethod
    def __get_not_equal_bound(bound, bounds_array):
        """
        Вернуть уникальную границу
        :param bound: Новая граница
        :param bounds_array: Существующие границы
        :return: bound, если она уникальна, иначе None
        """
        if bounds_array.count(bound) > 0:
            return None

        sub_str = bound[:bound.find("=") - 1]
        for b in bounds_array:
            if (sub_str + ">=") in b or (sub_str + "<=") in b:
                return None
        return bound

    @staticmethod
    def find_min(root):
        """
        Поиск наименьшего решения
        :param root: Корневой узел
        :return: Наименьшее решение
        """
        nods_array = BranchAndBorderMethod.__get_all_nodes(root)
        min_value = float("inf")
        variables = None

        for node in nods_array:
            if node.result < min_value:
                min_value = node.result
                variables = node.variables

        return min_value, variables

    @staticmethod
    def find_max(root):
        """
        Поиск наибольшего решения
        :param root: Корневой узел
        :return: Наибольшее решение
        """
        nods_array = BranchAndBorderMethod.__get_all_nodes(root)
        min_value = float("-inf")
        variables = None

        for node in nods_array:
            if node.result > min_value:
                min_value = node.result
                variables = node.variables

        return min_value, variables

    @staticmethod
    def __get_all_nodes(node, result=None):
        """
        Получение всех узлов, которые содержат решение
        :param node: Узел
        :param result: Массив всех узлов решений
        :return: Массив всех узлов решений
        """
        result = [] if result is None else result
        if BranchAndBorderMethod.__get_not_integer_var(node.variables)[0] == -1 \
                and not BranchAndBorderMethod.__is_contains_nulls(node.variables):
            result.append(node)

        if node.get_left() is not None:
            BranchAndBorderMethod.__get_all_nodes(node.get_left(), result)
        if node.get_right() is not None:
            BranchAndBorderMethod.__get_all_nodes(node.get_right(), result)

        return result


class Tree:
    def __init__(self, bound_array, function, optimal_model):
        self.root = Node(None, None, bound_array, function, optimal_model, 1)


class Node:
    def __init__(self, result, variables, bound_array, function, optimal_model, level=None, left=None, right=None):
        self.result = result  # Значение целевой функции
        self.variables = variables  # Значение всех переменных (x1...xn)
        self.bound_array = bound_array  # Ограничения на данном узле
        self.function = function  # Целевая функция
        self.optimal_model = optimal_model  # Оптимальная модель MAX/MIN
        self.level = level  # Уровень дерева
        self.left = left
        self.right = right

    def set_results(self, result, variables):
        self.result = result
        self.variables = variables

    def set_left(self, bound_array, new_bound, function, optimal_model, level):
        self.left = Node(None, None, bound_array + [new_bound], function, optimal_model, level)

    def set_right(self, bound_array, new_bound, function, optimal_model, level):
        self.right = Node(None, None, bound_array + [new_bound], function, optimal_model, level)

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bounds(self):
        return self.bound_array

    def get_function(self):
        return self.function

    def get_model(self):
        return self.optimal_model

    def __str__(self):
        return "Node [result = " + str(self.result) + ", vars = " + str(self.variables) \
               + ", level = " + str(self.level) \
               + ", borders = " + str(self.bound_array) \
               + "]"

    # + ", left = " + str(self.left is not None) \
    # + ", right = " + str(self.right is not None) \

    # def __str__(self):
    #     return "Node [fun = " + str(self.function) \
    #            + ", borders = " + str(self.bound_array) \
    #            + ", result = " + str(self.result) \
    #            + ", vars = " + str(self.variables) \
    #            + ", level = " + str(self.level) \
    #            + ", left = " + str(self.left) \
    #            + ", right = " + str(self.right) + "]"
