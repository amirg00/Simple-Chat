#
# Properties: Socket, name
import threading


class Client(threading.Thread):

    def __init__(self, name, socket, listening_socket):
        threading.Thread.__init__(self)
        self.__name = name
        self.__socket = socket
        self.__listening_socket = listening_socket

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
