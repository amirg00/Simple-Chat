# ---------PROTOCOL_MESSAGES--------#
# PROTOCOL CODES                    #
GET = "1"                           #
CONFIRM = "2"                       #
UPDATE = "3"                        #
ERROR = "4"                         #
                                    #
# PROTOCOL TYPE CODES               #
CONNECT_CODE = "00"                 #
DISCONNECT_CODE = "01"              #
USERS_LIST_CODE = "02"              #
SEND_MSG_CODE = "03"                #
SEND_BROADCAST_MSG_CODE = "04"      #
FILES_LIST_CODE = "05"              #
DOWNLOAD_FILE = "06"                #
# ----------------------------------#


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
        return username, port

    # for msg start with 201
    if type_code == DISCONNECT_CODE:
        return True

    # for msg start with 202
    if type_code == USERS_LIST_CODE:
        # reset list
        connected_users_list = []

        # check if there friends in chat right now
        users_exist = int(msg[:1])
        msg = msg[1:]

        # if firends exist, save them in list
        if users_exist:
            users_amount = int(msg[:1])
            msg = msg[1:]
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                msg = msg[username_len:]
                connected_users_list.append(username)  # update users list
        return connected_users_list

    # for msg start with 203
    if type_code == SEND_MSG_CODE:
        return True

    # for msg start with 204
    if type_code == SEND_BROADCAST_MSG_CODE:
        users_got_msg = []
        users_exist = int(msg[:1])
        msg = msg[1:]
        if users_exist:
            users_amount = int(msg[:1])
            msg = msg[1:]
            for i in range(users_amount):
                username_len = int(msg[:2])
                msg = msg[2:]
                username = msg[:username_len]
                msg = msg[username_len:]
                users_got_msg.append(username)

        return users_got_msg

    # for msg start with 205
    if type_code == FILES_LIST_CODE:
        files_list = []

        # check if there files in server chat
        files_exist = int(msg[:1])
        msg = msg[1:]

        # if files exist, save them in list
        if files_exist:
            files_amount = int(msg[:2])
            msg = msg[2:]
            for i in range(files_amount):
                filename_len = int(msg[:2])
                msg = msg[2:]
                filename = msg[:filename_len]
                msg = msg[filename_len:]
                files_list.append(filename)  # add file to list
        return files_list
        
    # for msg start with 206
    if type_code == DOWNLOAD_FILE:
        # get file size in bytes
        print(msg)
        file_size_field_len = int(msg[:2])
        msg = msg[2:]
        file_size = msg[:file_size_field_len]
        msg = msg[file_size_field_len:]
        # get port
        port = int(msg)
        
        return port, file_size


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
        return type_code, username

        # for msg start with 301
    if type_code == DISCONNECT_CODE:
        # take the friend that get out from chat
        username_len = int(msg[:2])
        msg = msg[2:]
        username = msg[:username_len]
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
        return type_code, username, new_msg


def analysis_errors_msg(type_code, msg):
    """
    Function analysis msg start with 4...
    thats messages says "An error is the response to your GET msg before."
    return the error id by protocol (RFC)
    """
    error_type = msg[:1]

    return ERROR, type_code, error_type


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
