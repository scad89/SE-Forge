import socket


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
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
            content = f'Method: {data[0]} Path: {data[1]} Params: {data[2]}'.encode(
                'utf-8')
            client_socket.send(HDRS.encode('utf-8') + content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
    finally:
        print('Server disconnected....')


start_server()
