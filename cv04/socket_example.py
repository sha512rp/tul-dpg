"""Sockets example in Python"""

import socket
import sys


SERVER_IP = 'localhost'
SERVER_PORT = 8090


def server_socket():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((SERVER_IP, SERVER_PORT))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    try:
        while True:
            connection, address = serversocket.accept()
            buf = connection.recv(64)
            if len(buf) > 0:
                print(buf.decode('utf-8'))
                continue
    except KeyboardInterrupt:
        pass
    finally:
        serversocket.close()


def client_socket():
    message = "hello"
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((SERVER_IP, SERVER_PORT))
    clientsocket.send(message.encode('utf-8'))


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if argv[1] == 'server':
        server_socket()
    elif argv[1] == 'client':
        client_socket()


if __name__ == '__main__':
    main()
