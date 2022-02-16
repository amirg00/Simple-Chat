import socket
from threading import Thread
#import logic

MIN_USERNAME_LEN = 4
MAX_USERNAME_LEN = 10

def is_valid_username(username):
    return MIN_USERNAME_LEN <= len(username) <= MAX_USERNAME_LEN


def main():
    
    # TODO: connect to server
    
    username = input("Hey, enter your username: ")
    
    if is_valid_username(username):
        # TODO: print menu
        
        # TODO: while choice is valid and not exit,
        #       send it to logic unit.
        
        