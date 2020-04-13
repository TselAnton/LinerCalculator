from api.BranchAndBorderMethod import BranchAndBorderMethod

fun = "3x1 + 5x2"
b1 = "5x1 + 2x2 <= 14"
b2 = "2x1 + 5x2 <= 16"
b3 = "x1 >= 1"
b4 = "x2 >= 1"
isMax = True

#TODO: Не поддерживаются символы '>' и '<'
#TODO: НЕ правильно считается значение целевой функции

print(BranchAndBorderMethod.find_solution(fun, [b1, b2, b3, b4], isMax))
