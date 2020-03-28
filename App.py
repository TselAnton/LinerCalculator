from api.parser import ParserException
from api.simplex import SimplexMethodSolver

fun = "30x1 + x2"
b1 = "90x1 + 5x2 <= 10000"
b2 = "x2 = 3x1"
num_const = 2

try:
    print(SimplexMethodSolver.find_solution(2, True, fun, [b1, b2]))
except ParserException as ex:
    print(ex.get_message())
except Exception as ex:
    print(str(ex))
