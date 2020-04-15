import tkinter.ttk as ttk
from tkinter import *

from api.BranchAndBorderMethod import BranchAndBorderMethod

limitations_text = []
limitations_entries = []
borders_labels = []


def number_of_limitations():
    global limitations_text
    global limitations_entries
    global borders_labels

    count_limitations_int = 0 if count_limitations_str == '' else int(count_limitations_str.get())
    limitations_text = [StringVar() for _ in range(count_limitations_int)]
    limitations_entries = [Entry(textvariable=limitations_text[i]) for i in range(count_limitations_int)]
    borders_labels = []
    for number in range(count_limitations_int):
        borders_labels.append(Label(text=str(number+1) + ") ", fg="#000000", bg=bg, font='Times 14'))
        borders_labels[number].grid(row=number + 2, column=0, sticky="e")
        limitations_entries[number].grid(row=number+2, column=1, padx=5, pady=5)


def BnP():
    global limitations_text
    global bnp_ordinary

    func = target_function_str.get()
    borders = [text.get() for text in limitations_text]
    optimal = (True if check.get() == 1 else False)

    result, timer = BranchAndBorderMethod.find_solution_with_time(func, borders, optimal)
    bnp_ordinary.entry["text"] = "Result = " + str(result[0]) + ", vars = " + str(result[1]) + ", time = " + str(timer)


def BnP_parall():
    global limitations_text
    global bnp_parallel

    func = target_function_str.get()

    borders = [text.get() for text in limitations_text]
    optimal = (True if check.get() == 1 else False)

    result, timer = BranchAndBorderMethod.find_solution_with_time(func, borders, optimal)
    bnp_parallel.entry["text"] = "Result = " + str(result[0]) + ", vars = " + str(result[1]) + ", time = " + str(timer)


#  цвет
bg = '#e7f2e1'
#  создание окна интерфейса
root = Tk()
root.configure(background=bg)
root.title("ЦЛП методом ветвей и границ")
root.geometry("1000x200")

s = ttk.Style()
s.configure('Wild.TRadiobutton', background=bg, foreground='black')

target_function_str = StringVar()
target_function = Label(text="Введите целевую функцию:", fg="#000000", bg=bg, font='Times 14')
target_function.grid(row=0, column=0, sticky="w")
# поле для записи целевой функции
target_function_entry = Entry(textvariable=target_function_str)
target_function_entry.grid(row=0, column=1, padx=5, pady=5)



# радио кнопка на мин или макс функции
check = IntVar()
max_radiobutton = ttk.Radiobutton(text="Max", style='Wild.TRadiobutton', value=1, variable=check)
max_radiobutton.grid(row=0, column=2, sticky="w")
min_radiobutton = ttk.Radiobutton(text="Min", style='Wild.TRadiobutton', value=2, variable=check)
min_radiobutton.grid(row=0, column=3, sticky="w")

count_limitations_str = StringVar()
count_limitations = Label(text="Количество ограничений:", fg="#000000", bg=bg, font='Times 14')
count_limitations.grid(row=1, column=0, sticky="w")
count_limitations_entry = Entry(textvariable=count_limitations_str)
count_limitations_entry.grid(row=1, column=1, padx=5, pady=5)

entering_limitations = Button(text="Ок", fg="#000000", bg="#c6f2ae", font='Times 14', command=number_of_limitations)
entering_limitations.grid(row=1, column=2, sticky="w")

entering_limitations = Button(text="Рандом", fg="#000000", bg="#c6f2ae", font='Times 14', command=number_of_limitations)
entering_limitations.grid(row=1, column=3, sticky="w")

bnp_str = StringVar()
#  кнопка для решения цлп методом ветвей и границ
bnp_ordinary = Button(text="Метод ветей и границ (один поток)", fg="#000000", bg="#c6f2ae", font='Times 14', command=BnP)
bnp_ordinary.grid(row=0, column=4, padx=25, pady=5, sticky="w")
bnp_ordinary.entry = Label(padx=0, pady=0, font='Times 14', bg=bg)
bnp_ordinary.entry.grid(row=0, column=5, padx=5, pady=5)

#  кнопка для решения цлп методом ветвей и границ параллельный
bnp_parallel = Button(text="Метод ветей и границ (параллельный)", fg="#000000", bg="#c6f2ae", font='Times 14', command=BnP_parall)
bnp_parallel.grid(row=1, column=4, padx=5, pady=5, sticky="w")
bnp_parallel.entry = Label(padx=0, pady=0, font='Times 14', bg=bg)
bnp_parallel.entry.grid(row=1, column=5, padx=5, pady=5)


#  Время работы алгоритма
time = Label(padx=0, pady=0, font='Times 14', bg="#e7f2e1")
time.grid(row=1, column=0, sticky=W, columnspan=3)
#  Сумма построенного маршрута
summs = Label(padx=0, pady=0, font='Times 14', bg=bg)
summs.grid(row=2, column=0, sticky=W, columnspan=3)
#  Проверка на некорректный ввод
stub1 = Label(font='Times 14', bg=bg, fg='red')
stub1.grid(row=3, column=0, sticky="w", columnspan=3)
#  Проверка на некорректный ввод
stub2 = Label(font='Times 14', bg=bg, fg='red')
stub2.grid(row=4, column=0, sticky="w", columnspan=3)
#  Проверка на некорректный ввод
output = Label(font='Times 14', bg=bg, fg='red')
output.grid(row=5, column=0, sticky="w", columnspan=3)
root.mainloop()
