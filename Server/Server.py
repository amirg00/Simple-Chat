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
            thread = Thread(target=self.clients_service, args=(client_socket,))
            thread.start()

    def clients_service(self, client_socket):
        message = client_socket.recv(1024).decode()
        print(message)
        response = self.analyse_data_by_protocol(message, client_socket)
        print(response)
        client_socket.send(response.encode())

    def analyse_data_by_protocol(self, message, client_socket):
        response = ""
        code = message[:3]
        print(message)
        print(code)
        if code == "100":
            username_len = message[3:5]
            USERNAME = message[5:]
            valid, status = self.check_valid_username(USERNAME)
            if valid:
                self.send_broadcast_message(300, USERNAME, username_len, "", "")
                self.__connected_clients[USERNAME] = Client(USERNAME, client_socket)
                response = f"200{username_len}{USERNAME}"
            else:
                response = f"400{status}"
            return response

        elif code == "101":
            print("request to logout...")
            deleted = False
            for k, v in self.__connected_clients.items():
                if v.get_socket() is client_socket:
                    del self.__connected_clients[k]
                    deleted = True
                    self.send_broadcast_message(301, k, self.fix_len(len(k)), "", "")
                    break
            return "201" if deleted else 1

        elif code == "102":
            print("request for the connected users' list...")
            Z = 0 if len(self.__connected_clients) == 0 else 1
            if Z == 0:
                return "20200"
            Y = len(self.__connected_clients)
            response = f"202{Z}{Y}"
            for user in self.__connected_clients:
                XX = len(user)
                if XX < 10:
                    XX = f"0{XX}"
                response += f"{XX}{user}"
            return response

        elif code == "103":
            target_username_len = int(message[3:5])
            target_USERNAME = message[5:target_username_len]
            MESSAGE_len = int(message[target_username_len:target_username_len + 2])
            MESSAGE = message[target_username_len + 2:]
            if target_USERNAME not in self.__connected_clients:
                response = f"403{1}"
                print("do something it is not valid!")
            else:
                self.__connected_clients[target_USERNAME].get_socket().send(MESSAGE.encode())
                response = "203"
            return response

        elif code == "104":
            broadcast_message_len = int(message[3:5])
            broadcast_message = message[5:]
            Z = 0 if len(self.__connected_clients) == 0 else 1
            if Z == 0:
                return "20400"
            Y = len(self.__connected_clients)
            response = f"204{Z}{Y}"
            for user, client in self.__connected_clients.items():
                client.get_socket().send(broadcast_message.encode())
                XX = len(user)
                response += f"{self.fix_len(XX)}{user}"
            return response

        elif code == "105":
            print("request for the files list of the server...")

        elif code == "106":
            file_size = int(message[3:5])
            FILENAME = message[5:]

    def check_valid_username(self, username: str):
        """
        The method checks whether the username is not already existed,
        and that his length doesn't descend 2.
        :param username: a given username.
        :return: true if the username is valid and can be added, o.w. returns false.
        """
        if len(username) < 2:
            return False, 1

        if username in self.__connected_clients:
            return False, 2

        if len(self.__connected_clients) == self.__users_max_amount:
            return False, 3

        return True, 0

    def send_broadcast_message(self, code, username, user_len, message, msg_len):
        if code == "300" or code == "301":
            for client in self.__connected_clients.values():
                client.get_socket().send(f"{code}{user_len}{username}")

        elif code == "303":
            for client in self.__connected_clients.values():
                client.get_socket().send(f"{code}{user_len}{username}{msg_len}{message}")

    def fix_len(self, XX: int):
        return f"0{XX}" if XX < 10 else f"{XX}"
