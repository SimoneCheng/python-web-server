from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from socket import socket
from parser.http_request_parser import HttpRequestParser

HOST = ""
PORT = 8888

listen_socket = socket(AF_INET, SOCK_STREAM)
listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

parser = HttpRequestParser()

print(f"Serving HTTP on port {PORT} ...")

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024).decode("utf-8")
    print(parser.feed_data(request_data))
    http_response = b"""\
        HTTP/1.1 200 OK
        Hello, World!
    """
    client_connection.sendall(http_response)
    client_connection.close()
