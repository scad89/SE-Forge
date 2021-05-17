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


def create_tables(connect, cursor):
    try:
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.execute("""CREATE TABLE currencies
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name text NOT NULL,
                      nbrb_id INTEGER NOT NULL)
                        """)
        cursor.execute("""CREATE TABLE rates
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        unit_cur INTEGER NOT NULL,
                        date text NOT NULL,
                        rate real NOT NULL,
                        currency_id INTEGER NOT NULL,
                        FOREIGN KEY (currency_id) REFERENCES currencies(id))
                        """)
    except Error:
        print(Error)
    finally:
        connect.commit()


def inserting_to_currencies(connect, curs):
    try:
        result_from_parsing = get_data()
        for i in result_from_parsing:
            curs.execute(
                "INSERT INTO currencies(name, nbrb_id) VALUES (?, ?)", (i['Cur_Name'], i['Cur_ID']))
    finally:
        connect.commit()


def inserting_to_rates_for_curent_date(connect, curs):
    try:
        list_id_from_currencies = return_id_currencies(curs)
        result_from_parsing = get_data()
        for i in result_from_parsing:
            curs.execute(
                "INSERT INTO rates(unit_cur, date, rate, currency_id) VALUES (?, ?, ?, ?)", (i['Cur_Scale'], (i['Date'].split('T')[0]), i['Cur_OfficialRate'], list_id_from_currencies[result_from_parsing.index(i)][0]))
    finally:
        connect.commit()


def get_data():
    list_of_currencies = [145, 355, 301, 298, 293, 290]
    parsing_data = []
    for i in list_of_currencies:
        response = requests.get(f'https://www.nbrb.by/api/exrates/rates/{i}')
        parsing_data.append(response.json())
    return parsing_data


def return_id_currencies(curs):
    curs.execute(
        'SELECT id, name FROM currencies')
    list_id = curs.fetchall()
    return list_id


def output_currencies(curs):
    curs.execute(
        'SELECT name FROM currencies')
    all_currencies = curs.fetchall()
    return all_currencies


def get_max_rate_into_data(curs):
    curs.execute(
        'SELECT unit_cur, date, rate FROM rates WHERE ID = (SELECT MAX(ID) FROM rates)')
    last_data_from_rates = curs.fetchall()
    return last_data_from_rates[0][0], last_data_from_rates[0][1], last_data_from_rates[0][2]


def find_rate_cur(curs, curval):
    curs.execute(
        "SELECT unit_cur, date, rate FROM rates WHERE (date = ?) and (id = ?)", (str(datetime.now().date()), curval))
    data_from_rates = curs.fetchall()
    unit, date, rate = check_return_sql_request(curs, data_from_rates)
    return unit, date, rate


def check_return_sql_request(curs, database_list):
    if database_list:
        return database_list[0][0], database_list[0][1], database_list[0][2]
    else:
        unit, date, rate = get_max_rate_into_data(curs)
        return unit, date, rate


def main():
    conn, curs = connect_to_database()
    questions_about_new_database = input(
        'Create tables of currencies and rates???(Y/N): ')
    if questions_about_new_database.lower() == 'y':
        create_tables(conn, curs)
        inserting_to_currencies(conn, curs)
    inserting_to_rates_for_curent_date(conn, curs)
    all_currencies = output_currencies(curs)
    for index, k in enumerate(all_currencies):
        print(f'{index+1}---{k[0]}')
    id_one_cur = int(input(
        'Введите номер валюты, которой хотите получить актуальный курс?(1, 2, 3...):  '))
    unit, date, rate = find_rate_cur(curs, id_one_cur)
    print(
        f'За {unit} {all_currencies[id_one_cur-1][0]} на дату {date} курс составляет {rate} BYN')
    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
