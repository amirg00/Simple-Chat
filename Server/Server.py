import socket
import threading
from threading import Thread
from Client import Client
from Protocol import Protocol
from RDT_Sender import RDT_Sender
import os

class Server:
    DESCRIPTION = """ This is the chat's server,
                      which responsible for responses for clients following the protocol.
                  """

    def __init__(self, ip, listening_port):
        """
            The constructor of the chat's server.

            Parameters
            ----------
            ip : str
                server's ip address.
            listening_port: int
                the port that the server listens to.

            Returns
            -------
            None
        """
        self.__ip = ip
        self.__listening_port = listening_port
        # server's listening socket.
        self.__listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # dictionary of all connected clients (key = username, value = Client)
        self.__connected_clients = {}
        # a class constant: maximum amount of allowed clients.
        self.__users_max_amount = 5
        # Files name list.
        self.__files = []
        # dictionary of allocated ports when: (key = port, value = True if port isn't taken, o.w. False)
        self.allocated_ports = {}
        for port in range(55000, 55031):
            self.allocated_ports[port] = True

    def start_listen(self) -> None:
        """
        Method which makes the server listening for incoming connections.
        Whenever there is a connection, the server make a thread for the method
        that offer a service for the client that has connected to the server.
        :return:
        """
        self.__listening_socket.bind(('', self.__listening_port))
        self.__listening_socket.listen(self.__users_max_amount)
        while True:
            client_socket, client_address = self.__listening_socket.accept()
            thread = Thread(target=self.clients_service, args=(client_socket,))
            thread.start()

    def clients_service(self, client_socket) -> None:
        """
        Method services the specific client through the client socket.
        It analyzes client's messages following the protocol, then sends
        back a corresponding response followed by the protocol.
        If users wants to disconnect, the client's socket is close, and loop
        breaks since there isn't a use of it anymore.
        :param client_socket: client's socket.
        :return: None
        """
        while True:
            message = client_socket.recv(1024).decode()
            print(message)
            try:
                if "\n" in message:
                    continue
            except:
                pass
            response = self.analyse_data_by_protocol(message, client_socket)
            if response is None:
                continue
            print(response)
            client_socket.send(response.encode())

            # If client decides to disconnect:
            if response[:3] == f"{Protocol.GET}{Protocol.DISCONNECT}":
                client_socket.close()
                break

    def analyse_data_by_protocol(self, message, client_socket) -> str:
        """
        Method analyses the client's message by the protocol.
        :param message: client's message.
        :param client_socket: client's socket.
        :return: the corresponding response string that the server will send back to the client.

        Notes
        ---------
        For more detailed information about our protocol, see in our repository,
        the pdf which elaborates about protocol's rules.
        """

        response = ""
        code = message[:3]
        print(message)
        # print(f"{Protocol.GET}")
        if code == f"{Protocol.GET}{Protocol.CONNECT}":
            username_len = message[3:5]
            USERNAME = message[5:]
            valid, status = self.check_valid_username(USERNAME)
            if valid:
                alloc_PORT = self.get_available_port()
                listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                listening_sock.bind(('', alloc_PORT))
                listening_sock.listen(1)
                response = f"{Protocol.CONFIRM}{Protocol.CONNECT}{username_len.zfill(2)}{USERNAME}{alloc_PORT}"
                client_socket.send(response.encode())
                client_socket_300, client_address = listening_sock.accept()
                # listening_sock.close()
                curr_client = Client(USERNAME, client_socket, client_socket_300, listening_sock)
                curr_client.set_PORT(alloc_PORT)
                self.__connected_clients[USERNAME] = curr_client
                self.send_broadcast_message(f"{Protocol.UPDATE}{Protocol.CONNECT}", USERNAME, username_len.zfill(2), "",
                                            "")
                response = None
            else:
                response = f"{Protocol.ERROR}{Protocol.CONNECT}{status}"
            return response

        elif code == f"{Protocol.GET}{Protocol.DISCONNECT}":
            print("request to logout...")
            deleted = False
            for user, client in self.__connected_clients.items():
                if client.get_socket() is client_socket:
                    self.redeem_user_port(user)
                    client.get_server_listening_socket().close()
                    client.get_listening_socket().close()
                    del self.__connected_clients[user]
                    deleted = True
                    self.send_broadcast_message(f"{Protocol.UPDATE}{Protocol.DISCONNECT}", user,
                                                self.fix_len(len(user)), "", "")
                    break
            return f"{Protocol.CONFIRM}{Protocol.DISCONNECT}" if deleted else 1

        elif code == f"{Protocol.GET}{Protocol.USERS_LIST}":
            print("request for the connected users' list...")
            Z = 0 if len(self.__connected_clients) == 1 else 1
            if Z == 0:
                return f"{Protocol.CONFIRM}{Protocol.USERS_LIST}{Z}"
            Y = len(self.__connected_clients) - 1
            response = f"{Protocol.CONFIRM}{Protocol.USERS_LIST}{Z}{Y}"
            for user, client in self.__connected_clients.items():
                print(f"{client.get_socket()}, {client_socket}")
                if client.get_socket() is client_socket:
                    continue
                XX = len(user)
                response += f"{self.fix_len(XX)}{user}"
            return response

        elif code == f"{Protocol.GET}{Protocol.SEND_MESSAGE}":
            target_username_len = int(message[3:5])
            message = message[5:]
            target_USERNAME = message[:target_username_len]
            message = message[target_username_len:]
            MESSAGE_len = message[:2]
            MESSAGE = message[2:]
            if target_USERNAME not in self.__connected_clients:
                response = f"{Protocol.ERROR}{Protocol.SEND_MESSAGE}{1}"
                print("do something it is not valid!")
            else:
                USERNAME = self.get_name_by_socket(client_socket)
                res_to_tar = f"{Protocol.UPDATE}{Protocol.SEND_MESSAGE}{self.fix_len(len(USERNAME))}{USERNAME}{MESSAGE_len.zfill(2)}{MESSAGE}"
                self.__connected_clients[target_USERNAME].get_listening_socket().send(res_to_tar.encode())
                response = f"{Protocol.CONFIRM}{Protocol.SEND_MESSAGE}"
            return response

        elif code == f"{Protocol.GET}{Protocol.SEND_BROADCAST_MESSAGE}":
            USERNAME = self.get_name_by_socket(client_socket)
            broadcast_message_len = message[3:5]
            broadcast_message = message[5:]
            Z = 0 if len(self.__connected_clients) == 1 else 1
            if Z == 0:
                return f"{Protocol.CONFIRM}{Protocol.SEND_BROADCAST_MESSAGE}{Z}"
            Y = len(self.__connected_clients) - 1
            response = f"{Protocol.CONFIRM}{Protocol.SEND_BROADCAST_MESSAGE}{Z}{Y}"
            for username, client in self.__connected_clients.items():
                if client.get_socket() is client_socket:
                    continue
                tar_msg = f"{Protocol.UPDATE}{Protocol.SEND_BROADCAST_MESSAGE}{self.fix_len(len(USERNAME))}{USERNAME}{broadcast_message_len.zfill(2)}{broadcast_message}"
                client.get_listening_socket().send(tar_msg.encode())
                XX = len(username)
                response += f"{self.fix_len(XX)}{username}"
            return response

        elif code == f"{Protocol.GET}{Protocol.FILES_LIST}":
            print("request for the files list of the server...")
            self.update_server_files()
            Z = 0 if len(self.__files) == 0 else 1
            if Z == 0:
                return f"{Protocol.CONFIRM}{Protocol.FILES_LIST}{Z}"
            YY = self.fix_len(len(self.__files))
            response = f"{Protocol.CONFIRM}{Protocol.FILES_LIST}{Z}{YY}"
            for file_name in self.__files:
                XX = self.fix_len(len(file_name))
                response += f"{XX}{file_name}"
            return response

        elif code == f"{Protocol.GET}{Protocol.DOWNLOAD_FILE}":
            PROTOCOL = message[3:6]
            FILENAME_len = message[6:8]
            FILENAME = message[8:]
            FILE_SIZE = os.path.getsize(f"./Files/{FILENAME}")
            FILE_SIZE_len = self.fix_len(len(str(FILE_SIZE)))
            allocated_port = self.get_available_port()
            response = f"{Protocol.CONFIRM}{Protocol.DOWNLOAD_FILE}{FILE_SIZE_len}{FILE_SIZE}{allocated_port}"
            client_socket.send(response.encode())

            if PROTOCOL == "UDP":
                rdt = RDT_Sender(allocated_port, f"./Files/{FILENAME}")
                sender_thread = Thread(target=rdt.main(), args=())
                sender_thread.start()
            else:
                pass  # here we will handle the TCP...

    def check_valid_username(self, username: str) -> (bool, int):
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

    def send_broadcast_message(self, code, username, user_len, message, msg_len) -> None:
        """
        Method sends through socket the broadcast message according the type (given code).
        :param code: a given broadcast code (could be 300, 301,...)
        :param username: a given client's username.
        :param user_len: the username length.
        :param message: the broadcast message.
        :param msg_len: the broadcast message length.
        :return: None
        """
        if code == f"{Protocol.UPDATE}{Protocol.CONNECT}" or code == f"{Protocol.UPDATE}{Protocol.DISCONNECT}":
            for user, client in self.__connected_clients.items():
                if user == username:
                    continue
                client.get_listening_socket().send(f"{code}{user_len}{username}".encode())

        elif code == f"{Protocol.UPDATE}{Protocol.SEND_MESSAGE}":
            for user, client in self.__connected_clients.items():
                if user == username:
                    continue
                client.get_listening_socket().send(f"{code}{user_len}{username}{msg_len}{message}".encode())

    def fix_len(self, XX: int):
        """
        Method fixes length to be with two digit whenever there is one.
        E.G.: for XX=3 -> return "03".
        :param XX: a given number.
        :return: string of the fixed int.
        """
        return f"0{XX}" if XX < 10 else f"{XX}"

    def get_name_by_socket(self, sock) -> str:
        """
        :param sock: a given socket.
        :return: the username which the given socket belongs to.
        """
        for username, value in self.__connected_clients.items():
            if value.get_socket() is sock:
                return username

    def get_available_port(self) -> int:
        """
        The method looks for a new available port, to allocate for the client's secondary socket.
        If there is an available port, then the function returns it, and right afterwards alters
        the port's value in the dictionary to False (means: this port is unavailable).
        If there is nothing to be found, i.e. there isn't a compatible port for the client,
        then we return that there is an error (-1 value).
        :return: the port which has allocated for the user sec's socket.
        """
        for port, available in self.allocated_ports.items():
            if available:
                self.allocated_ports[port] = False
                return port
        return -1

    def redeem_user_port(self, username) -> None:
        """
        Method redeems user's port after disconnecting from the server.
        :param username: a given username to redeem his port for other potential clients.
        :return: None
        """
        port = self.__connected_clients[username].get_PORT()
        self.allocated_ports[port] = True
        self.__connected_clients[username].set_PORT(-1)

    def update_server_files(self) -> None:
        """
        Method updates the files name list, according to the current server files.
        :return: None
        """
        self.__files.clear()
        for file_name in os.listdir("./Files"):
            self.__files.append(file_name)
