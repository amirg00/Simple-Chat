import socket
from threading import Thread
import logic
import analysis_unit

MIN_USERNAME_LEN = 4
MAX_USERNAME_LEN = 10

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345


def is_valid_username(username):
    return MIN_USERNAME_LEN <= len(username) <= MAX_USERNAME_LEN


def get_username():
    username = input("Hey, enter your username: ")

    while is_valid_username(username) is False:
        username = input("Invalid username, try again: ")

    return username


def get_choice():
    """
    Function print menu and ask option from user
    Input: None
    Output: user choice
    """
    choice = 0
    print("For send message to friend press 1")
    print("For send message to everyone press 2")
    print("For list of all connected friends press 3")
    print("For disconnect press 0")
    print()
    try:
        choice = int(input("So, what do you want? Enter option: "))
    except:
        choice = -1

    while not logic.MIN_OPTION <= choice <= logic.MAX_OPTION:
        try:
            choice = int(input("Invalid option. try again: "))
        except:
            choice = -1

    return choice


def listen_to_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (SERVER_IP, port)
    sock.connect(server_addr)

    while True:
        msg = sock.recv(1024).decode()
        ans = analysis_unit.analysis_msg_main(msg)
        if analysis_unit.CONNECT_CODE in ans:
            type_code, username = ans
            print(f"{username} add to chat")
        elif analysis_unit.DISCONNECT_CODE in ans:
            type_code, username = ans
            print(f"{username} leave the chat")
        elif analysis_unit.SEND_MSG_CODE in ans:
            type_code, username, msg = ans
            print(f"{username} to you: {msg}")
        elif analysis_unit.SEND_BROADCAST_MSG_CODE in ans:
            type_code, username, msg = ans
            print(f"{username} to everyone: {msg}")
        else:
            pass


def log_in_to_chat(sock):
    is_log_in = False

    while is_log_in is not True:
        username = get_username()
        msg = "100" + str(len(username)).zfill(2) + username
        sock.sendall(msg.encode())
        ans = sock.recv(1024).decode()
        ans = analysis_unit.analysis_msg_main(ans)
        if analysis_unit.ERROR in ans:
            code, type_code, type_error = ans
            if type_error == "1":
                print("Invalid username! try again.")
            elif type_code == "2":
                print("Username was taken! try again.")
            elif type_error == "3":
                print("Server full.. try later.")
                sock.close()
                exit()
            else:
                pass
        else:
            is_log_in = True

    username, port = ans
    print(f"Your username: {username} port for you: {port}")
    return port


def main():
    # connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (SERVER_IP, SERVER_PORT)
    sock.connect(server_addr)

    # enter to the chat as new friend inside
    port = log_in_to_chat(sock)

    # listen to incoming msg from server
    thread = Thread(target=listen_to_server, args=(port,))
    thread.start()

    # main loop for client
    choice = -1
    while (choice is not logic.EXIT_OPTION):
        choice = get_choice()
        logic.logic(choice, sock)


if __name__ == '__main__':
    main()
    #
