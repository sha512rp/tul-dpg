"""Exceptions for chat server."""


class RequestError(Exception):
    def __init__(self, message=''):
        super(RequestError, self).__init__('ERROR {:s}'.format(message))


class InvalidCommand(RequestError):
    def __init__(self, message=''):
        super(InvalidCommand, self).__init__('Invalid Command {:s}'.format(message))


class UsernameTaken(RequestError):
    def __init__(self, message=''):
        super(InvalidCommand, self).__init__('Username Taken {:s}'.format(message))
