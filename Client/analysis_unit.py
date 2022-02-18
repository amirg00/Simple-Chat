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

connected_users_list = []
  
def analysis_confirms_msg(type_code, msg):
    """
    Function analysis msg start with 2...
    thats messages says "Im OK msg to your previous GET msg"
    return value according to type_code...
    """
    
    # for msg start with 200
    if type_code == CONNECT_CODE:
        # take username
        username_len = int(msg[:2])
        msg = msg[2:]
        username = msg[:username_len]    
        msg = msg[username_len:]
        
        # take port from server
        port = int(msg[:])
        #print(f"Connect sucsses! username: {username} port for you at server: {port}") --TRY WITHOUT PRINTING
        return username, port
    
    # for msg start with 201
    if type_code == DISCONNECT_CODE:
        #print("Logout success.") --TRY WITHOUT PRINTING
        return True
    
    # for msg start with 202
    if type_code == USERS_LIST_CODE:
        # reset list
        global connected_users_list
        connected_users_list = []
        
        # check if there friends in chat rigth now
        users_exist = int(msg[:1])
        msg = msg[1:]
        
        # if firends exist, save them in list
        if users_exist:
            users_amount = int(msg[:1])
            msg = msg[1:]
            #print("Users in chat: ") --TRY WITHOUT PRINTING
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                msg = msg[username_len:]
                connected_users_list.append(username) # update users list
                #print(username) --TRY WITHOUT PRINTING
            return True
        else:
            #print("You are the only person in the chat!") --TRY WITHOUT PRINTING
            return False

    # for msg start with 203
    if type_code == SEND_MSG_CODE:
        #print("Your message was sent!") --TRY WITHOUT PRINTING
        return True
    
    # for msg start with 204
    if type_code == SEND_BROADCAST_MSG_CODE:
        users_got_msg = []
        users_exist = int(msg[:1])
        msg = msg[1:]
        if users_exist:
            users_amount = int(msg[:1])
            msg = msg[1:]
            #print("Users was get your message: ") --TRY WITHOUT PRINTING
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                msg = msg[username_len:]
                #print(username) --TRY WITHOUT PRINTING
                users_got_msg.append(username)

        return users_got_msg            

def analysis_updates_msg(type_code, msg):
    """
    Function analysis msg start with 3...
    thats messages says "new Friend get in, get out or you got new msg in chat"
    return value according to type_code...
    Note: if this function run, so it's from thread. (the listening unit)
    """
    
    # for msg start with 300
    if type_code == CONNECT_CODE:
        # take the new friend that connect to chat
        username_len = int(msg[:2])
        msg = msg[2:]  
        username = msg[:username_len]
        connected_users_list.append(username)
        
        return type_code, username       
    
    # for msg start with 301
    if type_code == DISCONNECT_CODE:
        # take the friend that get out from chat
        username_len = int(msg[:2])
        msg = msg[2:]  
        username = msg[:username_len]
        connected_users_list.remove(username)
        
        return type_code, username
    
    # for msg start with 303
    if type_code == SEND_MSG_CODE:
        username_len = int(msg[:2])
        msg = msg[2:]
        
        username = msg[:username_len]
        msg = msg[username_len:]
        
        new_msg_len = int(msg[:2])
        msg = msg[2:]

        new_msg = msg[:new_msg_len]
        #print(f"{username}: {new_msg}") --TRY WITHOUT PRINTING
        return type_code, username, new_msg

    # for msg start with 304
    if type_code == SEND_BROADCAST_MSG_CODE:
        username_len = int(msg[:2])
        msg = msg[2:]
        
        username = msg[:username_len]
        msg = msg[username_len:]
        
        new_msg_len = int(msg[:2])
        msg = msg[2:]

        new_msg = msg[:new_msg_len]
        #print(f"{username sent everyone}: {new_msg}") --TRY WITHOUT PRINTING
        return type_code, username, new_msg        
    
    
def analysis_errors_msg(type_code, msg):
    """
    Function analysis msg start with 4...
    thats messages says "An error is the response to your GET msg before."
    return the error id by protocol (RFC)
    """
    error_type = msg[:1]
       
    return (ERROR, type_code, error_type)    

def analysis_msg_main(msg):
    # get msg code
    code = msg[:1]
    msg = msg[1:]
    
    # get type of msg code
    type_code = msg[:2]
    msg = msg[2:]
    
    # goes to right function for next analysis by protocol msg code.
    if code == CONFIRM:
        return analysis_confirms_msg(type_code, msg)
    if code == UPDATE:
        return analysis_updates_msg(type_code, msg)
    if code == ERROR:
        return analysis_errors_msg(type_code, msg)
    
    print(f"Woops, error. this is msg make it: {code + type_code + msg}")
    exit()