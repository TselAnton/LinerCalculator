import math
import time
from threading import Thread

from api.Simplex import SimplexMethodSolver as simplex


class BranchAndBorderMethod:
    """
    Метод ветвей и границ
    """

    @staticmethod
    def find_solution_with_all_params(function, bounds_array, optimal_model, is_multiple_threads=False, expect_nulls=False, max_depth=10):
        return BranchAndBorderMethod \
            .__get_solution(function, bounds_array, optimal_model, is_multiple_threads, expect_nulls, max_depth)

    @staticmethod
    def find_solution_with_time(function, bounds_array, optimal_model, is_multiple_threads=False, expect_nulls=False, max_depth=10):
        result, work_time, depth = BranchAndBorderMethod \
            .__get_solution(function, bounds_array, optimal_model, is_multiple_threads, expect_nulls, max_depth)
        return result, work_time

    @staticmethod
    def find_solution(function, bounds_array, optimal_model, is_multiple_threads=False, expect_nulls=False, max_depth=10):
        return BranchAndBorderMethod\
            .__get_solution(function, bounds_array, optimal_model, is_multiple_threads, expect_nulls, max_depth)[0]

    @staticmethod
    def __get_solution(function, bounds_array, optimal_model, is_multiple_threads=False, expect_nulls=False, max_depth=10):
        """
        Поиск решения
        :param expect_nulls: Параметры который говорит, ожидаем ли мы нулевые значения
        :param max_depth: Максимальное количество слоёв дерева
        :param function: Целевая функция
        :param bounds_array: Ограничения
        :param optimal_model: Оптимальная модель
        :param is_multiple_threads: Использование нескольких потоков
        :return:
        """
        if is_multiple_threads is False:
            return BranchAndBorderMethod \
                .__find_solution_by_single_thread(function, bounds_array, optimal_model, max_depth, expect_nulls)
        else:
            return BranchAndBorderMethod\
                .__find_solution_by_multiple_threads(function, bounds_array, optimal_model, max_depth, expect_nulls)

    @staticmethod
    def __find_solution_by_multiple_threads(function, bounds_array, optimal_model, max_depth, expect_nulls):
        """
        Поиск решения в несколько потоков
        :param function: Целевая функция
        :param bounds_array: Ограничения
        :param optimal_model: Оптимальная модель
        :param max_depth: Максимальная глубина дерева
        :param expect_nulls: Ожидание нулевых значений
        :return: Результат, коэффициенты xn, время работы программы, максимальная глубина дерева
        """
        start_timer = time.time()
        tree = Tree(bounds_array, function, optimal_model)  # Создаём древовидную структуру

        main_thread = NewThread(tree.root, max_depth)
        main_thread.start()
        main_thread.join()
        tree = main_thread.get_result()

        return BranchAndBorderMethod.__find_max(tree, expect_nulls) \
            if optimal_model else BranchAndBorderMethod.__find_min(tree, expect_nulls), \
            time.time() - start_timer, BranchAndBorderMethod.__get_max_depth(tree)

    @staticmethod
    def __find_solution_by_single_thread(function, bounds_array, optimal_model, max_depth, expect_nulls):
        """
        Поиск решения в одиночном потоке
        :param function: Целевая функция
        :param bounds_array: Ограничения
        :param optimal_model: Оптимальная модель
        :param max_depth: Максимальная глубина дерева
        :param expect_nulls: Ожидание нулевых значений
        :return: Результат, коэффициенты xn, время работы программы, максимальная глубина дерева
        """
        start_timer = time.time()
        tree = Tree(bounds_array, function, optimal_model)  # Создаём древовидную структуру
        tree = BranchAndBorderMethod.__recount_node(tree.root, max_depth)  # Строим дерево

        return BranchAndBorderMethod.__find_max(tree, expect_nulls) \
            if optimal_model else BranchAndBorderMethod.__find_min(tree, expect_nulls), \
            time.time() - start_timer, BranchAndBorderMethod.__get_max_depth(tree)

    @staticmethod
    def __recount_node(node, max_depth):
        """
        Пересчитать значение в узле
        :param max_depth: Максимальная глубина дерева
        :param node: Узел дерева
        :return: Дерево решений
        """
        # Ищем решение
        result, variables = simplex.find_solution(node.get_function(), node.get_bounds(), node.get_model())
        node.set_results(result, variables)  # Задаём текущему узлу получившиеся значения

        float_value, float_num = BranchAndBorderMethod.get_not_integer_var(variables)  # Находим дробное значение

        if node.level < max_depth and result is not None:
            if float_num != -1:
                # Создаём доп ограничения
                left_bound, right_bound = BranchAndBorderMethod.create_new_bounds(float_value, float_num, node)

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
    def get_not_integer_var(variables):
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
    def create_new_bounds(value, num_of_x, node):
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
    def __get_max_depth(root):
        """
        Поиск высоты дерева
        :param root: Корневой узел
        :return: Высота дерева
        """
        nods_array = BranchAndBorderMethod.__get_all_nodes(root)
        max_depth = 0

        for node in nods_array:
            if node.level > max_depth:
                max_depth = node.level
        return max_depth

    @staticmethod
    def __find_min(root, expect_nulls):
        """
        Поиск наименьшего решения
        :param expect_nulls: Параметр ожидания нулевых значений
        :param root: Корневой узел
        :return: Наименьшее решение
        """
        nods_array = BranchAndBorderMethod.__get_all_results(root, expect_nulls)
        min_value = float("inf")
        variables = None

        for node in nods_array:
            if node.result is not None and node.result < min_value:
                min_value = node.result
                variables = node.variables

        return min_value, variables

    @staticmethod
    def __find_max(root, expect_nulls):
        """
        Поиск наибольшего решения
        :param expect_nulls: Параметр ожидания нулевых значений
        :param root: Корневой узел
        :return: Наибольшее решение
        """
        nods_array = BranchAndBorderMethod.__get_all_results(root, expect_nulls)
        min_value = float("-inf")
        variables = None

        for node in nods_array:
            if node.result is not None and node.result > min_value:
                min_value = node.result
                variables = node.variables

        return min_value, variables

    @staticmethod
    def __get_all_nodes(node, result=None):
        """
        Получение всех узлов
        :param node: Узел
        :param result: Массив всех узлов
        :return: Массив всех узлов
        """
        result = [] if result is None else result
        result.append(node)

        if node.get_left() is not None:
            BranchAndBorderMethod.__get_all_nodes(node.get_left(), result)
        if node.get_right() is not None:
            BranchAndBorderMethod.__get_all_nodes(node.get_right(), result)

        return result

    @staticmethod
    def __get_all_results(node, expect_nulls, result=None):
        """
        Получение всех узлов, которые содержат решение
        :param node: Узел
        :param result: Массив всех узлов решений
        :return: Массив всех узлов решений
        """
        result = [] if result is None else result
        if BranchAndBorderMethod.get_not_integer_var(node.variables)[0] == -1 \
                and (not expect_nulls or not BranchAndBorderMethod.__is_contains_nulls(node.variables)):
            result.append(node)

        if node.get_left() is not None:
            BranchAndBorderMethod.__get_all_results(node.get_left(), expect_nulls, result)
        if node.get_right() is not None:
            BranchAndBorderMethod.__get_all_results(node.get_right(), expect_nulls, result)

        return result


class NewThread(Thread):
    """
    Поток выполнения
    """
    def __init__(self, node, max_depth):
        Thread.__init__(self)
        self.name = "Thread [Level = " + str(node.level) + ", borders = " + str(node.bound_array) + "]"
        self.node = node
        self.max_depth = max_depth

    def run(self):
        """
        Функция расчёта значения узла
        """

        # Ищем решение
        result, variables = simplex.find_solution(self.node.get_function(), self.node.get_bounds(), self.node.get_model())
        self.node.set_results(result, variables)  # Задаём текущему узлу получившиеся значения

        float_value, float_num = BranchAndBorderMethod.get_not_integer_var(variables)  # Находим дробное значение

        if self.node.level < self.max_depth and result is not None:
            if float_num != -1:
                # Создаём доп ограничения
                left_bound, right_bound = BranchAndBorderMethod.create_new_bounds(float_value, float_num, self.node)

                if left_bound is not None:
                    # Создаём левый узел с дополнительным ограничением
                    self.node.set_left(self.node.get_bounds(), left_bound, self.node.get_function(),
                                       self.node.get_model(), self.node.level + 1)

                    left_thread = NewThread(self.node.get_left(), self.max_depth)
                    left_thread.start()
                    left_thread.join()

                if right_bound is not None:
                    # Создаём правый узел с дополнительным ограничением
                    self.node.set_right(self.node.get_bounds(), right_bound, self.node.get_function(),
                                        self.node.get_model(), self.node.level + 1)

                    right_thread = NewThread(self.node.get_right(), self.max_depth)
                    right_thread.start()
                    right_thread.join()

    def get_result(self):
        return self.node


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

