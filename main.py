import psycopg2
from pprint import pprint


# Функция, создающая структуру БД (таблицы)___________________________________________________________________________________функция
def create_db(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients (
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(40) UNIQUE
            );
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Telephones (
                tel_id SERIAL PRIMARY KEY,
                tel_number VARCHAR(40),
                client_id INTEGER NOT NULL REFERENCES Clients(client_id)
            );
        """)
    print('Таблицы созданы')

# Функция, позволяющая добавить нового клиента_________________________________________________________________________________функция
def add_new_client(cur, first_name, last_name, email, tel_number=None):
    cur.execute("""
        INSERT INTO Clients (first_name, last_name, email)
        VALUES (%s, %s, %s);
    """, (first_name, last_name, email))

    if tel_number: # проверка наличия телефона в функции, если есть, то:

        # получаем id последнего добавленного клиента, чтобы для него добавить телефон в таблицу Telephones:
        cur.execute("""
            SELECT client_id FROM clients WHERE first_name LIKE %s;
        """, (first_name,))
        client_id = cur.fetchone()[0]

        # добавляем телефон для последнего добавленного клиента
        cur.execute("""
            INSERT INTO Telephones (tel_number, client_id)
            VALUES (%s, %s);
        """, (tel_number, client_id))


# Функция, позволяющая добавить телефон для существующего клиента_______________________________________________________________функция
def add_telephone_for_client(cur, tel_number, client_id):

    # получаем все client_id
    cur.execute("""
            SELECT client_id FROM clients;
        """)
    id = cur.fetchall() # сохраняем кортажи в переменную
    for i in id: # проверка, что такой client_id уже существует
        if client_id in i:
            cur.execute("""
                INSERT INTO Telephones (tel_number, client_id)
                VALUES (%s, %s);
            """, (tel_number, client_id))
            result = 'Телефон добавлен для существующего клиента'
        else:
            result = 'C таким id клиента не существует'
    print(result)

# Функция, позволяющая изменить данные о клиенте________________________________________________________________________________функция
def change_client(cur, client_id, first_name=None, last_name=None, email=None, tel_number=None):
    # меняем имя client_id, если его передали в функцию
    if first_name:
        cur.execute("""
            UPDATE Clients
            SET first_name = %s
            WHERE client_id = %s;
        """, (first_name, client_id))

    # меняем фамилию client_id, если ее передали в функцию
    if last_name:
        cur.execute("""
            UPDATE Clients
            SET last_name = %s
            WHERE client_id = %s;
        """, (last_name, client_id))

    # меняем электронную почту client_id, если ее передали в функцию
    if email:
        cur.execute("""
            UPDATE Clients
            SET email = %s
            WHERE client_id = %s;
        """, (email, client_id))

    if tel_number: # проверка, что телефон передали в функцию

        # получаем количество телефонных номеров у данного client_id (len(tel_count))
        cur.execute("""
            SELECT tel_number FROM Telephones
            WHERE client_id = %s;
        """, (client_id, ))
        tel_count = cur.fetchall()
        if len(tel_count) > 1: # если у клиента client_id более одного телефона:
            yes = 0
            for i in tel_count:
                if tel_number in i: # поданый в функцию телефон уже есть в таблице
                    yes +=1
            print(yes)
            if yes == 0:
                # добавляем информацию о новом телефоне для клиента client_id:
                cur.execute("""
                    INSERT INTO Telephones (tel_number, client_id)
                    VALUES (%s, %s);
                """, (tel_number, client_id))
        elif len(tel_count) == 1: # у клиента уже имеется один телефон и значит его нужно поменять
            cur.execute("""
                UPDATE Telephones
                SET tel_number = %s
                WHERE client_id = %s;
            """, (tel_number, client_id))
            print('Телефонный номер обновлен')


# Функция, позволяющая удалить телефон для существующего клиента________________________________________________________________функция
def delete_tel(cur, client_id, tel_number):
    # получаем все client_id
    cur.execute("""
                SELECT client_id FROM clients;
            """)
    id = cur.fetchall()  # сохраняем кортажи в переменную
    for i in id:  # проверка, что такой client_id уже существует
        if client_id in i:
            cur.execute("""
                    DELETE FROM Telephones
                    WHERE tel_number = %s;
                """, (tel_number, ))


# Функция, позволяющая удалить существующего клиента_____________________________________________________________________________функция
def delete_client(cur, client_id):
    # получаем все client_id
    cur.execute("""
                SELECT client_id FROM clients;
            """)
    id = cur.fetchall()  # сохраняем кортажи в переменную
    for i in id:  # проверка, что такой client_id уже существует
        if client_id in i:
            cur.execute("""
                DELETE FROM Telephones
                WHERE client_id = %s;
            """, (client_id, ))
            cur.execute("""
                DELETE FROM Clients
                WHERE client_id = %s;
            """, (client_id, ))


# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону__________________________________________функция
def find_client(cur, first_name=None, last_name=None, email=None, tel_number=None):
    def get_from_clients(data):
        cur.execute("""
            SELECT first_name, last_name, email,client_id FROM Clients
            WHERE first_name = %s
            OR last_name = %s
            OR email = %s;
        """, (data, data, data))
        result_a = cur.fetchall()
        return result_a

    if first_name:
        result_a = get_from_clients(first_name)
    if last_name:
        result_a = get_from_clients(last_name)
    if email:
        result_a = get_from_clients(email)
    # print(result_a[0][3])
    cur.execute("""
        SELECT tel_number FROM Telephones
        WHERE client_id = %s;
    """, (result_a[0][3], ))
    result_b = cur.fetchall()
    # print(result_a)
    # print(result_b)
    tel_list = []
    for tel in result_b:
        tel_list.append(tel[0])
    print(f'Клиент {result_a[0][1]} {result_a[0][0]}, email: {result_a[0][2]}')
    print('Телефоны:')
    pprint(tel_list)







####_________________ВЫПОЛНЕНИЕ ПРОГРАММЫ_______________________________________________________________________________________программа
password = 'jNdL_2269' #input('Введите пароль от пользователя postgres: ')
conn = psycopg2.connect(database='homework', user='postgres', password=password)
with conn.cursor() as cur:
    # create_db(cur)
    # add_new_client(cur, 'Дмитрий', 'Черняев', 'dimitr_ch@mail.ru', '+7 927 264 22 69')
    # add_new_client(cur, 'Сергей', 'Мешков', 'sergey.meshkov@mail.ru', '+7 927 456 89 13')
    # add_new_client(cur, 'Александра', 'Пенькова', 'sanulya-krasotulya@mail.ru')
    # add_telephone_for_client(cur, '+7 927 600 09 12', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 13', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 14', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 15', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 16', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 17', 3)
    # add_telephone_for_client(cur, '+7 927 600 09 18', 7)
    # change_client(cur, 3, None, None, None, '+7 927 600 09 20')
    # change_client(cur, 2, None, None, None, '+7 927 600 09 21')
    # change_client(cur, 3, None, 'Черняева', None, None)
    # change_client(cur, 3, 'Сашулечка', 'Пенькова', None, None)
    # delete_tel(cur, 3, '+7 927 600 09 20')
    # delete_client(cur, 3)
    find_client(cur, 'Дмитрий', None, 'dimitr_ch@mail.ru')
    # find_client(cur, 'Сашулечка')
    # find_client(cur, None, 'Мешков')
conn.commit()
conn.close()












