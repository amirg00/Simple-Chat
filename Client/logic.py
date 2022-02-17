import analysis_unit as analysis
import socket

# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3

def users_list_handler():#(sock):
    #msg = analysis.GET + analysis.USERS_LIST_CODE
    #msg = msg.encode()
    #print(msg.decode())
    #sock.sendall(msg)
    #ans = sock.recv(1024).decode()
    #print(ans)
    #list_of_users = analysis.analysis_msg_main(ans)
    
    if(analysis.connected_users_list):
        print(f"user in the chat: {list_of_user}")
        return True
    else:
        print("You are the only user in the chat")
        return False
        
def send_msg_handler(sock):
    # build protocol msg to sent a msg to spesific client
    username = input("Enter user to sent him message: ")
    username_len = str(len(username))
    msg_to_user = input(f"Enter message for {username}: ")
    msg_to_user_len = str(len(msg_to_user))
    msg = analysis.GET + analysis.SEND_MSG_CODE + username_len.zfill(2) + username + msg_to_user_len.zfill(2) + msg_to_user
    msg = msg.encode()    
    print(msg.decode())
    
    # send it to server
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(analysis.analysis_msg_main(ans))

def send_msg_broadcast_handler(sock):
    msg_to_everyone = input("Enter message for everyone: ")
    msg_to_everyone_len = str(len(msg_to_user))
    msg = analysis.GET + analysis.SEND_BROADCAST_MSG_OPTION + msg_to_everyone_len.zfill(2) + msg_to_everyone
    msg = msg.encode() 
    print(msg.decode())
    # send it to server
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(analysis.analysis_msg_main(ans))

def logic(option, sock):
    if option is SEND_MSG_OPTION:
        send_msg_handler(sock)
    elif option is SEND_BROADCAST_MSG_OPTION:
        send_msg_broadcast_handler(sock)
    elif option is USERS_LIST_OPTION:
        users_list_handler()
    else:
        disconnect_handler(sock)
