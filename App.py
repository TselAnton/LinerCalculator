from api.parser import ParserException, Parser
from api.simplex import SimplexMethodSolver

fun = "-3x1 + x2 + 4x3"
b1 = "-x2 + x3 + x4 = 1"
b2 = "-5x1 + x2 + x3 = 2"
b3 = "-8x1 + x2 + 2x3 - x5 = 3"
num_const = Parser.find_max_constant([fun, b1, b2, b3])

# print(Parser.find_max_constant([fun, b1, b2, b3]))

try:
    print(SimplexMethodSolver.find_solution(num_const, True, fun, [b1, b2, b3]))
except ParserException as ex:
    print(ex.get_message())
