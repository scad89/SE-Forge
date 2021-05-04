import socket
import ssl
import json


def get_update_data():
    packet = "GET /api/exrates/currencies HTTP/1.1\r\nHost: www.nbrb.by\r\n\r\n".encode()
    client = socket.socket()
    client.connect(('www.nbrb.by', 443))
    client = ssl.wrap_socket(client, keyfile=None, certfile=None, server_side=False,
                             cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS)
    client.send(packet)
    data = ""
    while True:
        chunk = client.recv(4096).decode('utf-8', 'ignore')
        if chunk:
            data += chunk
        else:
            break
    data = data.split('\r\n\r\n')
    data = json.loads(data[1])
    with open("data_currency.json", "w") as file:
        json.dump(data, file, indent=2)


def print_all_money():
    with open('data_currency.json', 'r') as f:
        data = json.loads(f.read())
    for i in data:
        print("ID ", i["Cur_ID"], '-', "Currency ", i["Cur_Name"], sep=' ')
    return data


print('''
Так как сайт нашего Национального Банка организован по принципе"сервис по беларусску" и подключить API с актуальным курсами не представляется
возможным(https://www.nbrb.by/api/exrates/rates при переходе Not Found), будем выводить код валюты по ID.
''')
updating_data = input('Требуется ли скачать/обновить данные?(Y/N): ')
if updating_data.lower() == 'y':
    get_update_data()
list_money = print_all_money()
while True:
    cur_id = int(input('Введите id валюты, которой хотите узнать код: '))
    for i in list_money:
        if i['Cur_ID'] == cur_id:
            print('Код валюты', i['Cur_Name'], i['Cur_Code'])
            break
    else:
        print('Валюты с таким ID не найдено')
    question = input('Желаете продолжить?(Y/N): ')
    if question.lower() == 'n':
        break
