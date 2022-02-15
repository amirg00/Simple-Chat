#
# Properties: Socket, name
import threading


class Client(threading.Thread):

    def __init__(self, name, socket):
        threading.Thread.__init__(self)
        self.__name = name
        self.__socket = socket

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
