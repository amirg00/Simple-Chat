# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3


def listen_to_server()
    pass


def users_list_handler():
    msg = GET + USERS_LIST_CODE
    
    # TODO: sending msg to server,
    #       and get answer about users list.
    

def logic(option):
    if option is SEND_MSG_OPTION:
        send_msg_handler()
    elif option is SEND_BROADCAST_MSG_OPTION:
        send_msg_broadcast_handler()
    elif option is USERS_LIST_OPTION:
        users_list_handler()
    else:
        disconnect_handler()
