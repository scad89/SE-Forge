from contextlib import contextmanager, closing
import requests
import json
from datetime import datetime
import sqlite3
import contextlib

connect = sqlite3.connect('currencies.db')


@contextmanager
def connect_to_database():
    with contextlib.closing(connect.cursor()) as cursor:
        try:
            yield cursor
        except connect.DatabaseError:
            connect.rollback()
        else:
            connect.commit()


def create_tables():
    with connect_to_database() as cursor:
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


def inserting_to_currencies():
    with connect_to_database() as cursor:
        result_from_parsing = get_data()
        for i in result_from_parsing:
            cursor.execute(
                "INSERT INTO currencies(name, nbrb_id) VALUES (?, ?)", (i['Cur_Name'], i['Cur_ID']))


def inserting_to_rates_for_curent_date():
    with connect_to_database() as cursor:
        list_id_from_currencies = return_id_currencies()
        result_from_parsing = get_data()
        for i in result_from_parsing:
            cursor.execute(
                "INSERT INTO rates(unit_cur, date, rate, currency_id) VALUES (?, ?, ?, ?)", (i['Cur_Scale'], (i['Date'].split('T')[0]), i['Cur_OfficialRate'], list_id_from_currencies[result_from_parsing.index(i)][0]))


def get_data():
    list_of_currencies = [145, 355, 301, 298, 293, 290]
    parsing_data = []
    for i in list_of_currencies:
        response = requests.get(f'https://www.nbrb.by/api/exrates/rates/{i}')
        parsing_data.append(response.json())
    return parsing_data


def return_id_currencies():
    with connect_to_database() as cursor:
        cursor.execute(
            'SELECT id, name FROM currencies')
        list_id = cursor.fetchall()
        return list_id


def output_currencies():
    with connect_to_database() as cursor:
        cursor.execute(
            'SELECT name FROM currencies')
        all_currencies = cursor.fetchall()
        return all_currencies


def get_max_rate_into_data(curval):
    with connect_to_database() as cursor:
        cursor.execute(
            'SELECT unit_cur, date, rate FROM rates WHERE (id = ?)', (curval,))
        last_data_from_rates = cursor.fetchall()
        return last_data_from_rates[0][0], last_data_from_rates[0][1], last_data_from_rates[0][2]


def find_rate_cur(curval):
    with connect_to_database() as cursor:
        cursor.execute(
            "SELECT unit_cur, date, rate FROM rates WHERE (date = ?) and (id = ?)", (str(datetime.now().date()), curval))
        data_from_rates = cursor.fetchall()
        unit, date, rate = check_return_sql_request(data_from_rates, curval)
        return unit, date, rate


def check_return_sql_request(database_list, curval):
    if database_list:
        return database_list[0][0], database_list[0][1], database_list[0][2]
    else:
        unit, date, rate = get_max_rate_into_data(curval)
        return unit, date, rate


def main():
    questions_about_new_database = input(
        'Create tables of currencies and rates???(Y/N): ')
    if questions_about_new_database.lower() == 'y':
        create_tables()
        inserting_to_currencies()
    inserting_to_rates_for_curent_date()
    all_currencies = output_currencies()
    for index, k in enumerate(all_currencies):
        print(f'{index+1}---{k[0]}')
    id_one_cur = int(input(
        'Введите номер валюты, которой хотите получить актуальный курс?(1, 2, 3...):  '))
    unit, date, rate = find_rate_cur(id_one_cur)
    print(
        f'За {unit} {all_currencies[id_one_cur-1][0]} на дату {date} курс составляет {rate} BYN')
    connect.close()


if __name__ == '__main__':
    main()
