#
# Properties: Socket, name
import threading


class Client:

    def __init__(self, name, socket, listening_socket, server_listening_socket):
        self.__name = name
        self.__socket = socket
        self.__listening_socket = listening_socket
        self.__server_listening_socket = server_listening_socket
        self.__PORT = -1

    def get_name(self):
        """
        :return: client's name.
        """
        return self.__name

    def get_socket(self):
        """
        :return: client's socket.
        """
        return self.__socket

    def get_listening_socket(self):
        """
        :return: client's secondary socket, which listen for incoming (broadcast) chat messages.
        """
        return self.__listening_socket

    def get_server_listening_socket(self):
        return self.__server_listening_socket

    def get_PORT(self):
        """
        :return: user's listen socket port.
        """
        return self.__PORT

    def set_PORT(self, port):
        """
        :param port: a given port.
        :return: None
        """
        self.__PORT = port
