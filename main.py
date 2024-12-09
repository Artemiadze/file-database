from DataBase import *
import openpyxl


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

    # Ввод запроса в экран
    console = input("Введите команду\n")
    console = console.split()

    # Проверка на комманду
    if console[0].upper() == 'CREATE' and console[1].upper() == 'TABLE':
        create_empty_excel(columns=['ID', 'Name', 'Email', 'Group'], filename=f'{console[2]}.xlsx')
    if console[0].upper() == 'CREATE' and console[1].upper() == 'BACKUP':
        create_backup()
    elif console[0].upper() == 'INSERT':
        dataList = [int(console[1]), console[2] + " " + console[3], console[4], console[5]] if len(console) == 6 else \
            dataList = [int(console[1]), console[2], console[3], console[4]] # На случай, если вместо ФИ будет только Ф
        insert_excel(dataList)
    elif console[0].upper() == 'DELETE':
        delete_rows(console[1])  # 1 - это строка с названиями
    elif console[0].upper() == 'CLEAR':
        clean_database()
    elif console[0].upper() == 'PRINT':
        print_database()
        print_excel() if console[1].upper() == "student" else print_backup()
    elif console[0].upper() == 'SELECT':
        # печать строки по ключу
        get_data_to_ecxel(console[1]) if len(console) == 2 else get_data_to_ecxel(console[1], console[2])
        # иначе печать элемента из всей строки по ключу


