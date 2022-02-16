import socket
from threading import Thread
import logic

MIN_USERNAME_LEN = 4
MAX_USERNAME_LEN = 10


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
    choice = int(input("So, what do you want? Enter option: "))
    
    while not logic.MIN_OPTION <= choice <= logic.MAX_OPTION:
        choice = int(input("Invalid option. try again: "))
     
    return choice
    

def main():
    
    # TODO: connect to server
    
    username = get_username()
    
    # TODO: start thread for server updates by socket.
    
    if is_valid_username(username):
        choice = get_choice()
        print(f"your choice is: {choice}")
        
        # TODO: while choice is valid and not exit,
        #       send it to logic unit.
        

if __name__ == '__main__':
    main()