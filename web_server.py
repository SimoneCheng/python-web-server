from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from socket import socket
from parser.http_request_parser import HttpRequestParser
import json

HOST = ""
PORT = 8888

listen_socket = socket(AF_INET, SOCK_STREAM)
listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print(f"Serving HTTP on port {PORT} ...")

while True:
    client_connection, client_address = listen_socket.accept()
    parser = HttpRequestParser()
    request_data = client_connection.recv(1024).decode("utf-8")
    http_response = parser.feed_data(request_data)
    http_response_json = json.dumps(http_response, indent = 4)
    http_response_bytes = http_response_json.encode('utf-8')
    print(http_response_json)
    client_connection.sendall(http_response_bytes)
    client_connection.close()
