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
    elif console[0].upper() == 'CREATE' and console[1].upper() != 'TABLE':
        messagebox.showinfo('Создание', "Backup-файл базы данных создан")
        create_backup()
    elif console[0].upper() == 'INSERT':
        if len(console) == 6:
            dataList = [int(console[1]), console[2] + " " + console[3], console[4], console[5]]
        else:
            dataList = [int(console[1]), console[2], console[3], console[4]]  # На случай, если вместо ФИ будет только Ф
        insert_excel(dataList)
    elif console[0].upper() == 'DELETE':
        messagebox.showinfo("Удаление", f"Данные из строки {console[1] + 1} удалены")
        delete_rows(console[1] + 1)  # 1 - это строка с названиями(+1 - чтобы не удалили случайно строку с )
    elif console[0].upper() == 'REMOVE':
        if console[1] == "student":
            remove_database()
            messagebox.showinfo("Удаление базы данных", "База данных 'student' удалена успешно")
        else:
            remove_backup()
            messagebox.showinfo("Удаление backup-файла", "Backup-файл удалён успешно")
    elif console[0].upper() == 'CLEAR':
        clean_database()
        messagebox.showinfo("Очистка", "База данных очищена")
    elif console[0].upper() == 'PRINT':
        if console[1] == "student":
            print_database()
        else:
            print_backup()
    elif console[0].upper() == 'SELECT':
        # печать строки по ключу
        get_data_to_ecxel(console[1]) if len(console) == 2 else get_data_to_ecxel(console[1], console[2])
        # иначе печать элемента из всей строки по ключу


if __name__ == '__main__':
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


