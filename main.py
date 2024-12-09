from DataBase import *
from tkinter import *
from tkinter import messagebox
import openpyxl


def commit_commands():
    command = command_tf.get()
    console = command.split()
    # Проверка на комманду
    if console[0].upper() == 'CREATE' and console[1].upper() == 'TABLE':
        messagebox.showinfo('Создание', f"База данных {console[2]}.xlsx создана")
        create_empty_excel(columns=['ID', 'Name', 'Email', 'Group'], filename=f'{console[2]}.xlsx')
    if console[0].upper() == 'CREATE' and console[1].upper() == 'BACKUP':
        messagebox.showinfo('Создание', f"База данных {console[2]}.xlsx создана")
        create_backup()
    elif console[0].upper() == 'INSERT':
        if len(console) == 6:
            dataList = [int(console[1]), console[2] + " " + console[3], console[4], console[5]]
        else:
            dataList = [int(console[1]), console[2], console[3], console[4]]  # На случай, если вместо ФИ будет только Ф
        insert_excel(dataList)
        messagebox.showinfo("Добавление", "Ваши данные добавлены")
    elif console[0].upper() == 'DELETE':
        messagebox.showinfo("Удаление", f"Данные из строки {console[1] + 1} удалены")
        delete_rows(console[1] + 1)  # 1 - это строка с названиями(+1 - чтобы не удалили случайно строку с )
    elif console[0].upper() == 'CLEAR':
        clean_database()
        messagebox.showinfo("Очистка", "База данных очищена")
    elif console[0].upper() == 'PRINT':
        if console[1] == "student":
            print_database()
            print_excel()
        else:
            print_backup()
    elif console[0].upper() == 'SELECT':
        # печать строки по ключу
        get_data_to_ecxel(console[1]) if len(console) == 2 else get_data_to_ecxel(console[1], console[2])
        # иначе печать элемента из всей строки по ключу


if __name__ == '__main__':
    """
    create_empty_excel(columns=['ID', 'Name', 'Email', 'Group'], filename='student.xlsx')
    
    insert_excel([1, 'Vlasov Artyom', 'av@yandex.ru', '23CST2'])
    insert_excel([2, 'Igor Kim', 'i@yandex.ru', '23CST4'])
    insert_excel([3, 'Pedro Pascal', 'p@yandex.ru', '23CST10'])
    insert_excel([3, 'Pedro Pascal', 'p@yandex.ru', '23CST10'])  # - выведет, что уже есть такой элемент с таким id
    insert_excel([4, 'Arthur Morgan', 'a@yandex.ru', '23CST9'])
    
    get_data_to_ecxel("a@yandex.ru")  # печать строки по ключу
    get_data_to_ecxel("23CST10", "Name")  # печать элемента по ключу
    """

    window = Tk()  # Создаём окно приложения.
    window.title("SQL CONSOLE")  # Работа с БД
    window.geometry('700x200')
    frame = Frame(
        window,  # Обязательный параметр, который указывает окно для размещения Frame.
        padx=10,  # Задаём отступ по горизонтали.
        pady=10  # Задаём отступ по вертикали.
    )
    frame.pack(expand=True)  # Не забываем позиционировать виджет в окне. Здесь используется метод pack.
    # С помощью свойства expand=True указываем, что Frame заполняет весь контейнер, созданный для него.

    command_lb = Label(
        frame,
        text="Введите ваш запрос или нажмите кнопку  "
    )
    command_lb.grid(row=3, column=1)

    command_tf = Entry(
        frame,  # Используем нашу заготовку с настроенными отступами.
    )
    command_tf.grid(row=3, column=2)

    cal_btn = Button(
        frame,  # Заготовка с настроенными отступами.
        text='Выполнить',  # Надпись на кнопке.
        command=commit_commands
    )
    cal_btn.grid(row=5,
                 column=2)  # Размещаем кнопку в ячейке, расположенной ниже, чем наши надписи, но во втором столбце,
    # то есть под ячейками для ввода информации.
    window.mainloop()  # окно приложения не должно закрываться до тех пор, пока пользователь сам не сделает этого



