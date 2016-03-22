"""
Chatroom server in python, using sockets and threads

Welcome socket:
  - establish connection, get client name

Communication socket:
  - created when chatroom is entered for specific client
"""

from .chat_settings import SERVER_PORT, SERVER_IP
from .exceptions import RequestError, InvalidCommand, UsernameTaken
import socket


welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected_users = {}


def handle_request(request):
    command, *args = request.split(' ')
    if command == 'username':
        if len(args) >= 1:
            connect_user(args[1])
        else:
            raise InvalidCommand
    else:
        raise InvalidCommand


def connect_user(username):
    if username in connected_users:
        raise UsernameTaken
    print('Conntected User: {:s}'.format(username))


def main():
    welcome_socket.bind((SERVER_IP, SERVER_PORT))
    welcome_socket.listen(5)  # become a server socket, maximum 5 connections

    try:
        while True:
            connection, address = welcome_socket.accept()
            buf = connection.recv(64)  # TODO what is 64?
            if len(buf) > 0:
                request = buf.decode('utf-8')
                try:
                    handle_request(request)
                except RequestError as error:
                    connection.send(str(error))
                finally:
                    # TODO pass connection to other socket?
                    connection.close()
                continue
    except KeyboardInterrupt:
        pass
    finally:
        welcome_socket.close()
