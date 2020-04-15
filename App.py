from api.BranchAndBorderMethod import BranchAndBorderMethod

fun = "3x1 + 4x2"
b1 = "x1 + x2 <= 550"
b2 = "2x1 + 3x2 <= 1200"
b3 = "12x1 + 30x2 <= 9600"
isMax = True

#TODO: Генерпция линейных задач
# Возможно стоит проверять уровень глубины листа-решения, для оценки сгенерированной задачи (либо максимальгую глубину)

print(BranchAndBorderMethod.find_solution(fun, [b1, b2, b3], isMax, False))
print(BranchAndBorderMethod.find_solution_with_time(fun, [b1, b2, b3], isMax, False))
print(BranchAndBorderMethod.find_solution_with_all_params(fun, [b1, b2, b3], isMax, False))

print(BranchAndBorderMethod.find_solution(fun, [b1, b2, b3], isMax, True))
print(BranchAndBorderMethod.find_solution_with_time(fun, [b1, b2, b3], isMax, True))
print(BranchAndBorderMethod.find_solution_with_all_params(fun, [b1, b2, b3], isMax, True))
