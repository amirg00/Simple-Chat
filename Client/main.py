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
    
    # TODO: connect to server
    
    username = get_username()
    
    choice = -1
    
    while(choice is not logic.EXIT_OPTION):
        choice = get_choice()   
        logic.logic(choice)
        

if __name__ == '__main__':
    main()