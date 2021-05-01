import socket

URLS = ['tut.by', '4pda.ru', 'mail.ru', 'vk.com']


def output_head(data):
    dict_headers = {}
    for i in data:
        i = i.split(':', 1)
        if len(i) < 2:
            continue
        else:
            dict_headers[i[0]] = i[1]
    return dict_headers


def get_method_path_params(string):
    string = string.split(' ')
    path_and_params = ''
    if '?' not in string[1]:
        return string[0], string[1][1:], None
    else:
        path_and_params = string[1].split('?', 1)
        return string[0], path_and_params[0][1:], path_and_params[1]


def generate_answer(method, url):
    if method != 'GET':
        return ('Method not allowed', 405)
    if url.split('/', 1)[0] not in URLS:
        return('Not found', 404)
    return (('HTTP/1.1 200 OK\n\n', 200))


def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 8080))
        server.listen(4)
        print('Server connected...')
        while True:
            client_socket, adress = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            data = data.split('\n')
            headers = output_head(data[1:])
            method, path, params = get_method_path_params(data[0])
            headers_answer, code = generate_answer(method, path)
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n'
            if code == 200:
                headers_for_send = str(list(headers.keys())).encode('utf-8')
                request_line = f'Method: {method} \r\nPath: {path} \r\nParams: {params} \r\nHeaders: {headers_for_send}'.encode(
                    'utf-8')
            else:
                request_line = f'{code} \r\n {headers_answer}'.encode(
                    'utf-8')
            client_socket.sendall(HDRS.encode('utf-8')+request_line)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    finally:
        print('Server disconnected....')


start_server()
