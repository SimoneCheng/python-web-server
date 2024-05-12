import socket
from threading import Thread
import json
from datetime import datetime
from http_parser.http_request_parser import HttpRequestParser

host = ""
port = 8888

s = socket.socket()
s.bind((host, port))
s.listen(5)

print("Listening on " + str(host) + ":" + str(port))

def handle_connection(conn, addr):
    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            break
        parser = HttpRequestParser()
        response = parser.feed_data(data)
        response_json = json.dumps(response, indent = 4)
        response_bytes = response_json.encode('utf-8')
        print(response_json)
        conn.sendall(response_bytes)
    print("Connection closed: " + str(addr) + ", time:" + str(datetime.now()))
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connection from:" + str(addr) + ", time:" + str(datetime.now()))
    t = Thread(target=handle_connection, args=(conn, addr))
    t.start()

s.close()
