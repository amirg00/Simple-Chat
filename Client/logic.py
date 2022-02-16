import analysis_unit as analysis
import socket

# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3

def users_list_handler(sock):
    msg = analysis.GET + analysis.USERS_LIST_CODE
    msg = msg.encode()
    print(msg.decode())
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(ans)
    return analysis.analysis_msg_main(ans)

def send_msg_handler(sock):
    pass

def send_msg_broadcast_handler(sock):
    pass     

def logic(option, sock):
    if option is SEND_MSG_OPTION:
        send_msg_handler(sock)
    elif option is SEND_BROADCAST_MSG_OPTION:
        send_msg_broadcast_handler(sock)
    elif option is USERS_LIST_OPTION:
        users_list_handler(sock)
    else:
        disconnect_handler(sock)
