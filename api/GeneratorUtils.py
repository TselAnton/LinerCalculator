import random


class GeneratorUtils:

    @staticmethod
    def generate_liner_condition(num_of_args, left_border=-100, right_border=100):
        """
        Генерация ЦЛП задачи
        :param num_of_args: Количество аргументов
        :param left_border: Левая граница генерируемых чисел
        :param right_border: Правая граница генерируемых чисел
        :return: Целевая функция, ограничения
        """
        function = GeneratorUtils.__generate_left_part(num_of_args, left_border, right_border)
        borders = []

        for _ in range(num_of_args):
            borders.append(GeneratorUtils.__generate_left_part(num_of_args, left_border, right_border) +
                           GeneratorUtils.__generate_right_part(left_border, right_border))

        return function, borders

    @staticmethod
    def __generate_left_part(num_of_args, left_border, right_border):
        """
        Генерация левой части уравнения
        :param num_of_args: Количество аргументов
        :param left_border: Левая граница генерируемых чисел
        :param right_border: Правая граница генерируемых чисел
        :return: Левая часть уравнения
        """
        function = ""
        for arg_num in range(num_of_args):
            fun_cof = random.randint(left_border, right_border)
            function += ((str(fun_cof) if fun_cof < 0 else ("+" + str(fun_cof))) + "x" + str(arg_num + 1))

        return function

    @staticmethod
    def __generate_right_part(left_border, right_border):
        """
        Генерация правой части уравнения
        :param left_border: Левая граница генерируемых чисел
        :param right_border: Правая граница генерируемых чисел
        :return: Правая часть уравнения
        """
        fun_cof = random.randint(left_border, right_border)
        return ("<=" if fun_cof > 0 else ">=") + str(abs(fun_cof))
