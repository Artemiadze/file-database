# Лабораторная работа №2 #
## Файловая база данных на ЯП Python
***Выполнена студентом группы 23КНТ2 Власовым Артёмом Дмитриевичем***

Работа осущесвляется с помощью ЯП PYTHON, хранение данныых происходит в файлах EXCEL. Используются библиотеки pandas, openpyxl для работы с EXCEL файлами, OS для работы с устройством и tkinter для создания графического интерфейса. За основу берётся база данных из первой лабораторной работы для хранения данных о студенте. Она состоит из 4 полей: ID - ключевое (ID > 0), Name (String), Email (String), Group (String)

Запросы моего SQL надо писать в строке ввода в GUI и нажать на кнопку для выполнения скрипта. Данные скрипты sql под описаниями функции придуманны мной лично и выполняются только для данной программы.

# Алгоритмы
### 1. Создание БД
Функция для создания базы данных в формате файла Excel. Используется XlsxWriter в качестве движка для записи данных в файл Excel. В ходе выполнения фунцкии будет создана папка "Databases", если она ещё не создана, затем в данной папке создаётся БД в виде файла Excel с 4-мя столбцами, название которых передаётся в функцию, как и само название БД.

```
def create_empty_excel(columns: list, filename: str, sheet_name: str = 'Sheet1'):
    """ Функция создания базы данных в формате файлов Excel.
    Используется XlsxWriter в качестве движка для записи данных в файл Excel."""

    df = pd.DataFrame(columns=columns)  # Создание двумерной табличной структуры данных

    if not os.path.exists('Databases'):
        os.makedirs('Databases')

    filepath = os.path.join('Databases', filename)
    # используется XlsxWriter в качестве движка для записи данных в файл Excel.
    excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()  # Сохранения изменений в файле Excel
```

Cоответсвующий запрос:
```
CREATE TABLE student
```

### 2. Добавление новой записи в базу данных
Добавление в БД новую строку целиком, если её еще не было. Если уже есть строка с таким же ID то в систему будет возвращено сообщение "There is already a field with such a key value!", 
если записи с таким ID ещё не существует, то в БД добавится новая запись. Сложность алгоритма линейная, т.е. О(n), где n - кол-во строк в БД.

```
def insert_excel(information):
    """ Добавление в БД новую строку целиком, если её еще не было"""
    DB = openpyxl.load_workbook('Databases/student.xlsx')
    sheet = DB['Sheet1']
    
    # Проверка на отрицательность ключевого поля
    if information[0] < 0:
        messagebox.showinfo("Ошибка", "Значение ключевого поля не может быть отрицательным!")
        return
    info = parse_excel_to_dict_list('Databases/student.xlsx')
    flag = 0
    for i in info:
        # Проверка на наличие ID в БД
        if information[0] in i.values():
            messagebox.showinfo("Ошибка", "Уже существует такая запись с таким же ключом")
            flag = 1
    if flag == 0:
        messagebox.showinfo("Добавление", "Ваши данные добавлены")
        sheet.append(information)
    DB.save('Databases/student.xlsx')
```

Cоответсвующий запрос: 
```
INSERT 3 Pedro Pascal p@yandex.ru 23CST10
```

### 3. Извлечение данных из БД
Данный алгоритм реализуетяс через две функции: parse_excel_to_dict_list, get_data_to_ecxel. Функция parse_excel_to_dict_list берёт данные из БД и заносит в словарь для вывода на экран/поиска. Функция get_data_to_ecxel линейно ищет нужные строки по ключу, который в функцию передаёт пользователь. Функция находит все записи, совпадающие по значению с выводом на экран результатов поиска. Если пользователь помимо ключа вводит название стоблца который хочет вывести, то вместо всей строки с совпавшими данными выведется только значение из прописанного пользователем столбца. Сложность алгоритма линейная, т.е. О(n), где n - кол-во строк в БД.

```
def parse_excel_to_dict_list(filepath: str, sheet_name='Sheet1'):
    """Запись данных из таблицы в словари для вывода данных на экран или поиска данных"""

    # Загружаем Excel файл в DataFrame
    df = pd.read_excel(filepath, sheet_name=sheet_name)

    # Преобразовывает каждую строку DataFrame в словарь, в котором ключами служат названия столбцов.
    dict_list = df.to_dict(orient='records')

    return dict_list


def get_data_to_ecxel(parametr, colomn ="nothing"):
    """ Функция выводит данные из словаря, по ключу, сам словарь создан в функции parse_excel_to_dict_list"""

    info = parse_excel_to_dict_list('Databases/student.xlsx')
    print_GUI = ""
    # Заголовок для вывода только нужного элемента, где строка с совпавшим ключом
    if colomn != "nothing":
        print_GUI = colomn.upper()

    for i in info:
        if parametr in i.values():
            if colomn == "nothing":
                print_GUI = (print_GUI + "\n" + str(i["ID"]) + " " + str(i["Name"]) + " " + 
                             str(i['Email']) + " " + str(i['Group']))
            else:
                print_GUI = print_GUI + "\n" + str(i[colomn])
    messagebox.showinfo('Извлечение', print_GUI)
```

Соответствующий запрос:
```
SELECT "parametr" "Colomn_name"(опционально,если надо вывести конкретный столбец, а не всю строку)
SELECT a@yandex.ru
SELECT 23CST10 Name
```

### 4. Удаление столбца
Удаление из БД строки по её номеру происходит через индекс. Пользователь вводит номер строки, который хочет удалить, и компьютер удаляет запись с этим номером строки. Так как доступ к строке происходит по номеру, то алгоритм имеет сложность О(1).

```
def delete_rows(number_deleted_rows):
    """ Удаление из БД строки по её номеру"""
    DB = openpyxl.load_workbook('Databases/student.xlsx')
    sheet = DB['Sheet1']
    sheet.delete_rows(number_deleted_rows)
    DB.save('Databases/student.xlsx')
```

Соответствующий запрос:
```
DELETE "number_deleted_rows"
```

### 5. Очистка БД
Алгоритм очищает всю БД от данных, оставляя в наличии саму БД, но уже без данных. Сложность алгоритма линейная, т.е О(n), так как происходит удаление все строк от второй до последней.

```
def clean_database():
    """Очистка всей БД"""
    DB = openpyxl.load_workbook('Databases/student.xlsx')
    sheet = DB['Sheet1']
    sheet.delete_rows(2, sheet.max_row - 1)
    DB.save('Databases/student.xlsx')
```

Соответствующий запрос:
```
CLEAR
```

### 6. Вывод БД
Вывод всей БД. Сложность алгоритма линейная, т.е О(n)

```
def print_backup():
    """Печать всей БД"""
    DB = openpyxl.load_workbook('Databases/backup.xlsx')
    sheet = DB['Sheet1']
    print_to_console = ""
    for row in sheet.rows:
        string = ''
        for cell in row:
            string = string + str(cell.value) + ' '
        print_to_console = print_to_console + "\n" + string
    messagebox.showinfo('Таблица', print_to_console)
    DB.save('Databases/student.xlsx')
```

Соответствующий запрос:
```
PRINT student
```

### 7. Удаление БД
Алгоритм полного удаления БД из системы. Сложность алгоритма О(1)

```
def remove_database():
    """ Полное удаление БД из системы"""
    os.remove('Databases/student.xlsx')
```

Соответствующий запрос:
```
REMOVE student
```

### 8. Создание BACKUP-файла
Алгоритм создаёт новый файл, копирует данные из нашей БД в backup-файл и сохраняет всё. Сложность алгоритма О(1).

```
def create_backup():
    """ Создаёт Backup файл и сохраняет туда данные из нашей базы данных"""
    # Копируются данные из нашей БД
    data = pd.read_excel('Databases/student.xlsx', sheet_name="Sheet1")

    create_empty_excel(columns=['ID', 'Name', 'Email', 'Group'], filename='backup.xlsx')
    # Заполнение Backup файла нашими данными из BD
    data.to_excel('Databases/backup.xlsx', sheet_name='Sheet1')

    # удаление первого столбца ,в котором перечисляются индексы
    myFile = openpyxl.load_workbook('Databases/student.xlsx')
    sheet_myFile = myFile['Sheet1']
    sheet_myFile.delete_cols(1)
    myFile.save('Databases/student.xlsx')

    backupFile = openpyxl.load_workbook('Databases/backup.xlsx')
    sheet_backup = backupFile['Sheet1']
    sheet_backup.delete_cols(1)
    backupFile.save('Databases/backup.xlsx')
```

Соответствующий запрос:
```
CREATE BACKUP
```

### 9. Вывод backup-файла
Вывод содержимого из backup-файла. Сложность алгоритма линейная, т.е О(n)

```
def print_backup():
    """Печать всей БД"""
    DB = openpyxl.load_workbook('Databases/backup.xlsx')
    sheet = DB['Sheet1']
    print_to_console = ""
    for row in sheet.rows:
        string = ''
        for cell in row:
            string = string + str(cell.value) + ' '
        print_to_console = print_to_console + "\n" + string
    messagebox.showinfo('Таблица', print_to_console)
    DB.save('Databases/student.xlsx')
```

Соответствующий запрос:
```
PRINT backup
```

### 10. Удаление 
Алгоритм полного удаления backup-файла из системы. Сложность алгоритма О(1)

```
def remove_backup():
    """Полное удаление backup-файла из системы"""
    os.remove('Databases/backup.xlsx')
```

Соответствующий запрос:
```
REMOVE backup
```