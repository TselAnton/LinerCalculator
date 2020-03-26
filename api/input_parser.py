class Parser:
    LESS = "<"
    LESS_OR_EQUAL = "<="
    EQUAL = "="
    MORE = ">"
    MORE_OR_EQUAL = ">="

    # Map для всех символов и их порядкого номера в КА
    SYMBOLS = {
        "+": 0, "-": 0, "0": 1, "1": 1, "2": 1,
        "3": 1, "4": 1, "5": 1, "6": 1, "7": 1,
        "8": 1, "9": 1, ".": 2, ",": 2, "x": 3,
        "*": 4, "<": 5, ">": 5, "=": 6, None: 7
    }

    # Расшифровка всех ошибок
    EXCEPTIONS = {
        "US": "Неожиданный символ '{}'",
        "UF": "Формула не закночена!",
        "UC": "Неизвестный символ '{}'"
    }
    # Переменная окончания парсинга
    END_OF_PARSING = "EP"

    # Расшифровки к ошибкам:
    # US — Unexpected symbol (Неожиданный символ)
    # UF — Unfinished formula (Незаконченная формула)
    # UC - Unknown character (Неизвестный символ)
    # EP — End Of Parsing (Конец парсинга: выход из программы)
    STATES = [
        [   1,    2, 'US',    5, 'US', 'US', 'US', 'UF'],     # 0 — Начало ввода
        ['US',    2, 'US',    5, 'US', 'US', 'US', 'UF'],     # 1 — Ввод знака перед числом
        ['US',    2,    3,    5,    4, 'US', 'US', 'UF'],     # 2 — Ввод числа перед иксом
        ['US',    2, 'US', 'US', 'US', 'US', 'US', 'UF'],     # 3 — Ввод точки в числе перед иксом
        ['US', 'US', 'US',    5, 'US', 'US', 'US', 'UF'],     # 4 — Ввод умножения
        ['US',    6, 'US', 'US', 'US', 'US', 'US', 'UF'],     # 5 — Ввод икса
        [   1,    6, 'US', 'US', 'US',    7,    8, 'EP'],     # 6 — Ввод номера икса
        ['US',    9, 'US', 'US', 'US', 'US',    8, 'UF'],     # 7 — Ввод знака больше или меньше
        ['US',    9, 'US', 'US', 'US', 'US', 'US', 'UF'],     # 8 — Ввод знака равенства
        ['US',    9,   10, 'US', 'US', 'US', 'US', 'EP'],     # 9 — Ввод числа после знаков условия
        ['US',    9, 'US', 'US', 'US', 'US', 'US', 'UF']      # 10 — Ввод точки в числе после знаков условия
    ]

    # TODO Будет массив коэффициентов [0 1 2 3] для [x1 x2 x3 x4]
    # TODO Отдельно будет условие, и значение после него. А потом они подставляются в формулу

    @staticmethod
    def parse_function(str_func, const_array, is_border):
        str_func = str_func.replace(" ", "")
        before_state = 0   # Предыдущее состояние
        new_state = 0   # Следующее состояние
        cof_array = [0 in range(len(const_array))]  # Массив коэффициентов

        last_cof = None     # Последний считанный коэффициент
        last_x_numb = None  # Последний номер икса

        for i in range(len(str_func)):  # Читаем строку посимвольно
            current_char = str_func[i]  # Берём текущую строку

            if Parser.SYMBOLS.__contains__(current_char):       # Если в таблице символов данный символ поддерживается
                new_state = Parser.STATES[before_state][Parser.SYMBOLS[current_char]]   # Берём новое состояние

                if new_state == "US":   # Если мы перешли в неправильное состояние, выдаём ошибку
                    raise ParserException(Parser.EXCEPTIONS["US"].format(current_char))

                # TODO
                if before_state < 4 and (new_state == 4 or new_state == 5):
                    pass

                # TODO: Обрабатывать
                pass
            else:
                raise ParserException(Parser.EXCEPTIONS["UC"].format(current_char))     # Иначе вызываем ошибку

            before_state = new_state    # Обновляем предыдущее состояние КА

        if Parser.STATES[before_state][Parser.SYMBOLS[None]] == Parser.END_OF_PARSING:  # Если мы вышли из КА
            # TODO: Добавить проверку на наличие граничных условий
            return "Working!"
        else:
            raise ParserException(Parser.EXCEPTIONS["UF"])  # Формула не закончена, вызываем ошибку


class ParserException(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)

    def get_message(self):
        return self.message
