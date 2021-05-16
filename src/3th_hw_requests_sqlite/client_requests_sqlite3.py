import requests
import json
from datetime import datetime
import sqlite3
from sqlite3 import Error


def connect_to_database():
    try:
        connect_sqlite = sqlite3.connect('currencies.db')
        print('Connection to SQLite DB successful')
    except connect_sqlite.DatabaseError:
        print('SQLite DB connection error')
    else:
        try:
            cursor = connect_sqlite.cursor()
        except (connect_sqlite.IntegrityError, connect_sqlite.ProgrammingError, connect_sqlite.OperationalError) as e:
            connect_sqlite.rollback()
            print('Error: ', e.args)
    finally:
        if connect_sqlite:
            return connect_sqlite, cursor


def create_table(connect, cursor):
    try:
        cursor.execute("""CREATE TABLE rates
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      currency text,
                      date text,
                      rate real)
                        """)
    except Error:
        print(Error)
    finally:
        connect.commit()


def get_rate_for_current_data(connect_for_insert, cursor):
    response = requests.get('https://www.nbrb.by/api/exrates/rates/145')
    dict_currency_rate = response.json()
    inserting_data_into_database(
        connect_for_insert, cursor, dict_currency_rate)


def inserting_data_into_database(connect, curs, dict_parsing):
    try:
        curs.execute("INSERT INTO rates(currency, date, rate) VALUES (?, ?, ?)",
                     (dict_parsing['Cur_Name'], (dict_parsing['Date'].split('T')[0]), dict_parsing['Cur_OfficialRate']))
    finally:
        connect.commit()


def get_max_rate_into_data(curs):
    curs.execute(
        'SELECT currency, date, rate FROM rates WHERE ID = (SELECT MAX(ID) FROM rates)')
    rows = curs.fetchall()
    return rows[0][1], rows[0][2], rows[0][3]


def output_current_rate(curs):
    curs.execute("SELECT * FROM rates WHERE date = ?",
                 (str(datetime.now().date()),))
    rows = curs.fetchall()
    cur, date, rate = check_return_sql_request(curs, rows)
    return cur, date, rate


def check_return_sql_request(curs, database_list):
    if database_list:
        return database_list[0][1], database_list[0][2], database_list[0][3]
    else:
        cur, date, rate = get_max_rate_into_data(curs)
        return cur, date, rate


def main():
    conn, curs = connect_to_database()
    questions_about_new_database = input('Create a table of rates??(Y/N): ')
    if questions_about_new_database.lower() == 'y':
        create_table(conn, curs)
    get_rate_for_current_data(conn, curs)
    name, data, rate = output_current_rate(curs)
    print(f'Курс {name} на дату {data} составляет {rate} BYN')
    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
