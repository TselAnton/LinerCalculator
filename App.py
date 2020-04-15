from api.GeneratorUtils import GeneratorUtils
from api.BranchAndBorderMethod import BranchAndBorderMethod


def generate_solution(num_of_args):
    is_normal = False
    while not is_normal:
        fun, borders = GeneratorUtils.generate_liner_condition(num_of_args)

        result, time, depth = BranchAndBorderMethod.find_solution_with_all_params(fun, borders, True, False, False, num_of_args + 5)
        if depth >= num_of_args:
            print("На максимум:")
            print("Один поток: ", BranchAndBorderMethod.find_solution_with_time(fun, borders, True, False))
            print("Несколько потоков: ", BranchAndBorderMethod.find_solution_with_time(fun, borders, True, True))

            print("На минимум:")
            print("Один поток: ", BranchAndBorderMethod.find_solution_with_time(fun, borders, False, False))
            print("Несколько потоков: ", BranchAndBorderMethod.find_solution_with_time(fun, borders, False, True))
            is_normal = True


generate_solution(9)  # Номер — количество переменных x