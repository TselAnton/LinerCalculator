from api.parser import Parser, ParserException

try:
    pass
except ParserException as ex:
    print(ex.get_message())