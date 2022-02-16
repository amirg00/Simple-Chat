import analysis_unit as analysis

# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3

def users_list_handler():
    msg = analysis.GET + analysis.USERS_LIST_CODE
    
    # TODO: sending msg to server,
    #       and get answer about users list,
    #       and send it to analysis.

def send_msg_handler():
    pass

def send_msg_broadcast_handler():
    pass     

def logic(option):
    if option is SEND_MSG_OPTION:
        send_msg_handler()
    elif option is SEND_BROADCAST_MSG_OPTION:
        send_msg_broadcast_handler()
    elif option is USERS_LIST_OPTION:
        users_list_handler()
    else:
        disconnect_handler()
