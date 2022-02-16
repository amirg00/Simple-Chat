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
    
def analysis_confirms_msg(type_code, msg):
    if type_code is CONNECT_CODE:
        username_len = int(msg[:2])
        msg = msg[2:]
        username = msg[:username_len]    
        print(f"Connect to server sucsses! your username is {username}")
        return True
    
    if type_code is DISCONNECT_CODE:
        print("Logout success.")
        return True
    
    if type_code is USERS_LIST_CODE:
        users_exist = int(msg[:1])
        msg = msg[1:]
        if users_exist:
            users_amount = msg[:1]
            msg = msg[1:]
            print("Users in chat: ")
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                print(username)
            return True
        else:
            print("You are the only person in the chat!")
            return False
    
    if type_code is SEND_MSG_CODE:
        print("Your message was sent!")
        return True
    
    if type_code is SEND_BROADCAST_MSG_CODE:
        users_exist = int(msg[:1])
        msg = msg[1:]
        if users_exist:
            users_amount = msg[:1]
            msg = msg[1:]
            print("Users was get your message: ")
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                print(username)
            return True
        else:
            print("You are the only person in the chat!")
            return False    

def analysis_updates_msg(type_code, msg):
    if type_code is SEND_MSG_CODE:
        username_len = int(msg[:2])
        msg = msg[2:]
        
        username = msg[:username_len]
        msg = msg[username_len:]
        
        new_msg_len = msg[:2]
        msg = msg[2:]

        new_msg = msg[:new_msg_len]
        print(f"{username}: {new_msg}")
        return True    
    
    
def analysis_errors_msg(type_code, msg):
    pass

def analysis_msg_main(msg):
    # get msg code
    code = msg[:1]
    msg = msg[1:]
    
    # get type of msg code
    type_code = msg[:2]
    msg = msg[2:]
    
    if code is CONFIRM:
        return analysis_confirms_msg(type_code, msg)
    if code is UPDATE:
        return analysis_updates_msg(type_code, msg)
    if code is ERROR:
        return analysis_errors_msg(type_code, msg)
    
    printf(f"Woops, error. this is msg make it: {code + type_code + msg}")
    exit()