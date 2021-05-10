import requests
import json
from datetime import datetime
import sqlite3
from sqlite3 import Error


def create_database():
    try:
        conn = sqlite3.connect("currencies.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE rates
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      currency text,
                      date text,
                      rate real)
                        """)
    except Error:
        print(Error)
    finally:
        conn.commit()
        conn.close()


def get_rate_for_current_date():
    response = requests.get('https://www.nbrb.by/api/exrates/rates/145')
    dict_currency_rate = response.json()
    return inserting_data_into_database(dict_currency_rate)


def inserting_data_into_database(dict):
    try:
        conn = sqlite3.connect("currencies.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rates(currency, date, rate) VALUES (?, ?, ?)",
                       (dict['Cur_Name'], (dict['Date'].split('T')[0]), dict['Cur_OfficialRate']))
    finally:
        conn.commit()
        conn.close()


def check_date():
    try:
        conn = sqlite3.connect("currencies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rates WHERE date = ?",
                       (str(datetime.now().date()),))
        rows = cursor.fetchall()
        check_return_sql_request(rows)
    finally:
        conn.commit()
        conn.close()


def check_return_sql_request(list):
    if len(list) == 0:
        get_rate_for_current_date()


def output_current_rate():
    try:
        conn = sqlite3.connect("currencies.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rates WHERE date = ?",
                       (str(datetime.now().date()),))
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute(
                'SELECT currency, date, rate FROM rates WHERE ID = (SELECT MAX(ID) FROM rates)')
            output_rate = cursor.fetchall()
            return output_rate[0][1], output_rate[0][2], output_rate[0][3]
        else:
            return rows[0][1], rows[0][2], rows[0][3]
    finally:
        conn.commit()
        conn.close()


def main():
    questions_about_new_database = input('Создать базу данных?(Y/N): ')
    if questions_about_new_database.lower() == 'y':
        create_database()
    check_date()
    name, date, rate = output_current_rate()
    print(f'Курс {name} на дату {date} составляет {rate} BYN')


if __name__ == '__main__':
    main()
