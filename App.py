from api.BranchAndBorderMethod import BranchAndBorderMethod

fun = "3x1 + 5x2"
b1 = "5x1 + 2x2 <= 14"
b2 = "2x1 + 5x2 <= 16"
isMax = True

print(BranchAndBorderMethod.find_solution(fun, [b1, b2], isMax, False))
