from api.input_parser import Parser, ParserException
from api.simplex_method import find_solution

try:
    Parser.parse_function(" -50 * x1 + x2", 5)
except ParserException as ex:
    print(ex.get_message())