#
# Properties: ip,listening port,
#             listening socket,
#             connected clients dict (key = client's name : value = client's ref).
#
#

import socket
from threading import Thread
from Client import Client
import time


class Server:

    def __init__(self, ip, listening_port):
        self.__ip = ip
        self.__listening_port = listening_port
        self.__listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connected_clients = {}
        self.__users_max_amount = 5

    def start_listen(self):
        self.__listening_socket.bind(('', self.__listening_port))
        self.__listening_socket.listen(self.__users_max_amount)
        while True:
            client_socket, client_address = self.__listening_socket.accept()
            ip, port = client_address
            thread = Thread(target=self.print_something, args=(port, 3, ))
            thread.start()
            print("Simha hello")

    def print_something(self, s: str, t: int):
        for i in range(1, 11):
            print(f"src port = {s}")
            time.sleep(t)

    # def clients_service(self, client_socket):


