class Parser:

    # Константы границ
    __LESS = "<"
    __LESS_OR_EQUAL = "<="
    __EQUAL = "="
    __MORE = ">"
    __MORE_OR_EQUAL = ">="

    # Лист всех границ
    __BORDERS = [__LESS, __LESS_OR_EQUAL, __EQUAL, __MORE, __MORE_OR_EQUAL]

    # Map для всех символов и их порядкого номера в КА
    __SYMBOLS = {
        "+": 0, "-": 0, "0": 1, "1": 1, "2": 1,
        "3": 1, "4": 1, "5": 1, "6": 1, "7": 1,
        "8": 1, "9": 1, ".": 2, ",": 2, "*": 3,
        "x": 4, None: 5
    }

    # Расшифровки к ошибкам:
    # US — Unexpected symbol (Неожиданный символ)
    # UF — Unfinished formula (Незаконченная формула)
    # UC - Unknown character (Неизвестный символ)
    # BCE — No boundary conditions (Отсутсвуют граничные условия)
    __EXCEPTIONS = {
        "US": "Неожиданный символ '{}'",
        "UF": "Формула не закночена!",
        "UC": "Неизвестный символ '{}'",
        "BCE": "Отсутсвуют граничные условия"
    }

    # Переменная окончания парсинга
    # EP — End Of Parsing (Конец парсинга: выход из программы)
    __END_OF_PARSING = "EP"

    # Таблица состояний (КА)
    __STATES = [
        [   1,    2, 'US', 'US',    5, 'UF'],     # 0 — Вход в конечный автомат
        ['US',    2, 'US', 'US',    5, 'UF'],     # 1 — Знак перед числом (+/-)
        ['US',    2,    3,    4,    5, 'EP'],     # 2 — Ввод числа
        ['US',    2, 'US', 'US', 'US', 'UF'],     # 3 — Ввод точки в числе перед иксом
        ['US', 'US', 'US', 'US',    5, 'UF'],     # 4 — Ввод умножения
        ['US',    6, 'US', 'US', 'US', 'UF'],     # 5 — Ввод икса
        [   0,    6, 'US', 'US', 'US', 'EP']      # 6 — Ввод номера икса
    ]

    """
    Парсить функию с граничными условиями
    Пример: 2*x1 + 3*x2 >= 100
    Пример: 2*x1 + 3*x2 = 4*x3
    
    str_func — Функция в виде строки
    const_count — Количество констант X
    """
    @staticmethod
    def parse_function_with_borders(str_func, const_count):
        str_func = str_func.replace(" ", "")

        # Проверяем, есть ли граничные условия
        if not Parser.__is_contains_borders(str_func):
            raise ParserException(Parser.__EXCEPTIONS["BCE"])

        # Задаём левые и правые части формулы
        left_side, right_side, border = Parser.__split_formula(str_func)

        left_cof, left_free_cof = Parser.__parse_side_of_function(left_side, const_count)
        right_cof, right_free_cof = Parser.__parse_side_of_function(right_side, const_count)

        return [left_cof, right_cof], [left_free_cof, right_free_cof], border

    """
    Парсить функию без граничных условий
    Пример: 2*x1 + 3*x2
    Пример: 2*x1 + 3*x2 - 4*x3
    
    str_func — Функция в виде строки
    const_count — Количество констант X
    """
    @staticmethod
    def parse_alone_function(str_func, const_count):
        str_func = str_func.replace(" ", "")
        return Parser.__parse_side_of_function(str_func, const_count)

    """
    Парсинг одной части
    """
    @staticmethod
    def __parse_side_of_function(str_func, const_count):
        before_state = 0   # Предыдущее состояние
        new_state = 0   # Следующее состояние

        cof_array = [0 in range(len(const_count))]  # Массив коэффициентов
        free_cof = None   # Свободный коэффициент

        buffer = None   # Буффер для значений
        buffered_cof = None     # Последний сохранённый коэффициент

        for i in range(len(str_func)):  # Читаем строку посимвольно
            current_char = str_func[i]  # Берём текущую строку

            if Parser.__SYMBOLS.__contains__(current_char):       # Если в таблице символов данный символ поддерживается
                new_state = Parser.__STATES[before_state][Parser.__SYMBOLS[current_char]]   # Берём новое состояние

                if new_state == "US":   # Если мы перешли в неправильное состояние, выдаём ошибку
                    raise ParserException(Parser.__EXCEPTIONS["US"].format(current_char))

                # Если мы записывали всё это время число
                if Parser.__is_input_number(before_state, new_state):
                    buffer = current_char if buffer is None else (buffer + current_char)

                # Если мы наткнулись на 'x'
                elif new_state == 5:
                    buffered_cof = Parser.__resolve_to_float(buffer)
                    buffer = None

                # Если мы ввели номер икса
                elif before_state == 6 and new_state == 0:
                    cof_array[int(buffer)] = buffered_cof
                    buffered_cof = None
                    buffer = None
            else:
                raise ParserException(Parser.__EXCEPTIONS["UC"].format(current_char))     # Иначе вызываем ошибку

            before_state = new_state    # Обновляем предыдущее состояние КА

        if len(buffer) != 0:
            free_cof = float(buffer)

        if Parser.__STATES[before_state][Parser.__SYMBOLS[None]] == Parser.__END_OF_PARSING:  # Если мы вышли из КА
            return cof_array, free_cof
        else:
            raise ParserException(Parser.__EXCEPTIONS["UF"])  # Формула не закончена, вызываем ошибку

    """
    Проверочный метод, содержит ли строка граничные знаки
    """
    @staticmethod
    def __is_contains_borders(str_func):
        for border in Parser.__BORDERS:
            if border in str_func:
                return True
        return False

    """
    Возвращает разделённую строку по граничному знаку
    """
    @staticmethod
    def __split_formula(str_func):
        for border in Parser.__BORDERS:
            if border in str_func:
                return str_func.split(border)[0], str_func.split(border)[1], border

    """
    Проверяем вводим ли мы число
    """
    @staticmethod
    def __is_input_number(old_state, new_state):
        if old_state == new_state \
                or old_state < 4 and new_state < 4 \
                or old_state == 5 and new_state == 6:
            return True
        return False

    @staticmethod
    def __resolve_to_float(str_num):
        if str_num == "-":
            return -1
        elif str_num == "+":
            return 1
        else:
            return float(str_num)


class ParserException(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)

    def get_message(self):
        return self.message
