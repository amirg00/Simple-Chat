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
    

def main():
    
    # connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (SERVER_IP, SERVER_PORT)
    sock.connect(server_addr)
    
    # get username for chat
    username = get_username()
    
    # connect to chat
    msg = "100" + str(len(username)).zfill(2) + username
    print(msg)
    sock.sendall(msg.encode())
    ans = sock.recv(1024).decode()
    print(ans)
    #ans = "20006simcha" # until server will fixed for this msg
    
    while analysis_unit.analysis_msg_main(ans) is not True:
        username = get_username()
    
    # main loop for client
    choice = -1
    while(choice is not logic.EXIT_OPTION):
        choice = get_choice()   
        logic.logic(choice, sock)
        

if __name__ == '__main__':
    main()