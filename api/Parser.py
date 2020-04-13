import re


class Parser:
    """
    Парсер входных функций
    :author Kuvshinova Evgenia
    """
    # Константы границ
    LESS = "<"
    LESS_OR_EQUAL = "<="
    EQUAL = "="
    MORE = ">"
    MORE_OR_EQUAL = ">="

    # Лист всех границ
    __BORDERS = [LESS_OR_EQUAL, MORE_OR_EQUAL, LESS, EQUAL, MORE]

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
        [1, 2, 'US', 'US', 5, 'UF'],        # 0 — Вход в конечный автомат
        ['US', 2, 'US', 'US', 5, 'UF'],     # 1 — Знак перед числом (+/-)
        ['US', 2, 3, 4, 5, 'EP'],           # 2 — Ввод числа
        ['US', 2, 'US', 'US', 'US', 'UF'],  # 3 — Ввод точки в числе перед иксом
        ['US', 'US', 'US', 'US', 5, 'UF'],  # 4 — Ввод умножения
        ['US', 6, 'US', 'US', 'US', 'UF'],  # 5 — Ввод икса
        [0, 6, 'US', 'US', 'US', 'EP']      # 6 — Ввод номера икса
    ]

    @staticmethod
    def parse_function_with_borders(str_func, const_count):
        """
        Парсить функию с граничными условиями
                Пример: 2*x1 + 3*x2 >= 100
                Пример: 2*x1 + 3*x2 = 4*x3
        :param str_func: Функция в виде строки
        :param const_count: Количество используемых констант
        :return: Массив векторов коэффициентов для левой и правой части,
        массив свободных членов для левой и правой части
        """
        str_func = str_func.replace(" ", "")

        # Проверяем, есть ли граничные условия
        if not Parser.__is_contains_borders(str_func):
            raise ParserException(Parser.__EXCEPTIONS["BCE"])

        # Задаём левые и правые части формулы
        left_side, right_side, border = Parser.__split_formula(str_func)

        left_cof, left_free_cof = Parser.__parse_side_of_function(left_side, const_count)
        right_cof, right_free_cof = Parser.__parse_side_of_function(right_side, const_count)

        return [left_cof, right_cof], [left_free_cof, right_free_cof], border

    @staticmethod
    def parse_alone_function(str_func, const_count):
        """
        Парсить функию без граничных условий
                Пример: 2*x1 + 3*x2
                Пример: 2*x1 + 3*x2 - 4*x3
        :param str_func: Функция в виде строки
        :param const_count: Количество используемых констант
        :return: Вектор коэффициентов, свободный член
        """
        str_func = str_func.replace(" ", "")
        return Parser.__parse_side_of_function(str_func, const_count)

    @staticmethod
    def find_max_constant(func_array):
        """
        Парсит целевую функцию и все ограничения, для нахождения
        наибольшего номера X
        :param func_array: Массив с целевой функцией и всех ограничений
        :return: Номер наибольшего X
        """
        pattern = "x\\d+"
        max_num = 0

        for str_func in func_array:
            for num in re.findall(pattern, str_func):
                if int(num[1:]) > max_num:
                    max_num = int(num[1:])

        return max_num

    @staticmethod
    def __parse_side_of_function(str_func, const_count):
        """
        Парсинг одной части функции
        :param str_func: Часть функции в виде строки
        :param const_count: Количество используемых констант
        :return: Вектор коэффициентов, свободный член
        """
        before_state = 0  # Предыдущее состояние
        new_state = 0  # Следующее состояние

        cof_array = [0 for _ in range(const_count)]  # Массив коэффициентов
        free_cof = None  # Свободный коэффициент

        buffer = None  # Буффер для значений
        buffered_cof = None  # Последний сохранённый коэффициент

        for i in range(len(str_func)):  # Читаем строку посимвольно
            current_char = str_func[i]  # Берём текущую строку

            if Parser.__SYMBOLS.__contains__(current_char):  # Если в таблице символов данный символ поддерживается
                new_state = Parser.__STATES[before_state][Parser.__SYMBOLS[current_char]]  # Берём новое состояние

                if new_state == "US":  # Если мы перешли в неправильное состояние, выдаём ошибку
                    raise ParserException(Parser.__EXCEPTIONS["US"].format(current_char))

                # Если нужно запомнить текущий символ в буффер
                if Parser.__is_need_to_save_char(before_state, new_state):
                    buffer = current_char if buffer is None else (buffer + current_char)

                # Если нужно записать коэффициент в буффер
                elif Parser.__is_need_update_cof_buffer(before_state, new_state):
                    buffered_cof = Parser.__resolve_to_float(buffer)
                    buffer = None

                # Если нужно записать коэффициент в массив
                elif Parser.__is_needed_to_save_cof(before_state, new_state):
                    cof_array[int(buffer) - 1] = buffered_cof
                    buffered_cof = None
                    buffer = current_char
            else:
                raise ParserException(Parser.__EXCEPTIONS["UC"].format(current_char))  # Иначе вызываем ошибку

            before_state = new_state  # Обновляем предыдущее состояние КА

        if len(buffer) != 0 and buffered_cof is not None:
            cof_array[int(buffer) - 1] = buffered_cof
        elif len(buffer) != 0 and buffered_cof is None:
            try:
                free_cof = float(buffer)
            except ValueError:
                raise ParserException(Parser.__EXCEPTIONS["UF"])  # Формула не закончена, вызываем ошибку

        if Parser.__STATES[before_state][Parser.__SYMBOLS[None]] == Parser.__END_OF_PARSING:  # Если мы вышли из КА
            return cof_array, free_cof
        else:
            raise ParserException(Parser.__EXCEPTIONS["UF"])  # Формула не закончена, вызываем ошибку

    @staticmethod
    def __is_needed_to_save_cof(old_state, new_state):
        """
        Проверка на необходимость обнулить буфер
        :param old_state:
        :param new_state:
        :return:
        """
        if old_state == 6 and new_state == 0:
            return True
        return False

    @staticmethod
    def __is_need_update_cof_buffer(old_state, new_state):
        """
        Проверка на необходимость записать значение из буфера в буфер коэфициентов
        :param old_state: Предыдущее состояние
        :param new_state: Новое состояние
        :return: True — обновить буфер / False — не обновлять буфер
        """
        if (old_state == 2 and (new_state == 4 or new_state == 5)) or (old_state < 2 and new_state == 5):
            return True
        return False

    @staticmethod
    def __is_need_to_save_char(old_state, new_state):
        """
        Проверка на необходимость записать текущий символ в буффер
        * Это происходит только при запоминании чисел
        :param old_state: Предыдущее состояние
        :param new_state: Новое состояние
        :return: True — записать символ в буффер / False — не записывать число в буффер
        """
        if old_state == new_state \
                or old_state < 4 and new_state < 4 \
                or old_state == 5 and new_state == 6:
            return True
        return False

    @staticmethod
    def __is_contains_borders(str_func):
        """
        Проверочный метод, содержит ли строка граничный знак
        :param str_func: Функция в виде строки
        :return: True — строка содержит граничный знак / False — не содержит
        """
        for border in Parser.__BORDERS:
            if border in str_func:
                return True
        return False

    @staticmethod
    def __split_formula(str_func):
        """
        Делит строку по граничному знаку ('>', '<', '>=', '<=', '=')
        :param str_func: Функция в виде строки
        :return: Левая часть функции, правая часть функции, разделяющий знак
        """
        for border in Parser.__BORDERS:
            if border in str_func:
                return str_func.split(border)[0], str_func.split(border)[1], border

    @staticmethod
    def __resolve_to_float(str_num):
        """
        Перевод строки в число
        Если на вход придёт строка, содержащая только знак "+" или "-",
        то вернуться соотвественно "+1" и "-1"
        :param str_num: Число в виде строки
        :return: Число float
        """
        if str_num is None:
            return 1
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
