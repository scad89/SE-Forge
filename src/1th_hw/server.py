import socket
import re


def output_head(data):
    dict_head = {}
    ls = []
    buf = ''
    our_key = ''
    for i in data:
        if 'HTTP/1.1' in buf:
            buf = ''
        if i == '\n':
            ls.append(buf)
            buf = ''
        else:
            buf += i

    for i in ls:
        for j in range(len(i)):
            if i[j] == ':':
                new_key = our_key.replace('\r', '')
                dict_head[new_key] = i[j+1:]
                our_key = ''
                break
            else:
                our_key += i[j]
    return dict_head


def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8080))
        server.listen(4)
        print('Server connected...')
        while True:
            client_socket, adress = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            headers = output_head(data)
            print(data)
            print(adress)
            data = data.split()
            headers_for_send = str(list(headers.keys())).encode('utf-8')
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
            request_line = f'Method: {data[0]} Path: {data[1][1:]} Params: {data[2]}'.encode(
                'utf-8')
            client_socket.send(HDRS.encode('utf-8') +
                               request_line + headers_for_send)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    finally:
        print('Server disconnected....')


start_server()
