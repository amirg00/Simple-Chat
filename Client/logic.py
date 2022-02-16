# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3

#---------PROTOCOL_MESSAGES--------#
# PROTOCOL CODES                   #
GET = "1"                          #
CONFIRM = "2"                      #
UPDATE = "3"                       #
ERROR = "4"                        #
                                   #
# PROTOCOL TYPE CODES              #
CONNECT_CODE = "00"                #
DISCONNECT_CODE = "01"             #
USERS_LIST_CODE = "02"             #
SEND_MSG_CODE = "03"               #
SEND_BROADCAST_MSG_CODE = "04"     #
#----------------------------------#

def analysis_msg_main(msg):
    # get msg code
    code = msg[:1]
    msg = msg[1:]
    
    # get type of msg code
    type_code = msg[:2]
    msg = msg[2:]
    
    if code is GET:
        analysis_get_msg(type_code)
    elif code is CONFIRM:
        analysis_confirm_msg(type_code)
    elif code is UPDATE:
        analysis_updates_msg(type_code)
    elif code is ERROR:
        analysis_confirm_msg(type_code)
    else:
        printf(f"Woops, error. this is msg make it {code + type_code + msg}")
        exit()


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
