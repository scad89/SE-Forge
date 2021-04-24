import socket
import requests


def output_head(link):
    return link.headers


def check_body(link):
    return link.request.body


def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8080))
        server.listen(4)
        print('Server connected...')
        while True:
            client_socket, adress = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            data = data.split()
            response = requests.get('https:/'+data[1])
            headers = output_head(response)
            body = check_body(response)
            headers_for_send = str(list(headers.keys())).encode('utf-8')
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
            request_line = f'Method: {data[0]} Path: {data[1][1:]} Params: {data[2]} Body: {body}'.encode(
                'utf-8')
            client_socket.send(HDRS.encode('utf-8') +
                               request_line + headers_for_send)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    finally:
        print('Server disconnected....')


start_server()
