import analysis_unit as analysis
import socket

# options
SEND_MSG_OPTION = 1
SEND_BROADCAST_MSG_OPTION = 2
USERS_LIST_OPTION = 3
FILES_LIST_OPTION = 4
DOWNLOAD_OVER_UDP = 5
DOWNLOAD_OVER_TCP = 6
EXIT_OPTION = 0

MIN_OPTION = 0
MAX_OPTION = 3


def download_over_tcp_handler(sock, filename):
    msg = analysis.GET + analysis.DOWNLOAD_FILE
    msg += "TCP"
    msg += str(len(filename)).zfill(2) + filename
    msg = msg.encode()
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    return analysis.analysis_msg_main(ans)


def download_over_udp_handler(sock, filename):
    msg = analysis.GET + analysis.DOWNLOAD_FILE
    msg += "UDP"
    msg += str(len(filename)).zfill(2) + filename
    msg = msg.encode()
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    return analysis.analysis_msg_main(ans)


def files_list_handler(sock):
    msg = analysis.GET + analysis.FILES_LIST_CODE
    msg = msg.encode()
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    return analysis.analysis_msg_main(ans)


def users_list_handler(sock):
    msg = analysis.GET + analysis.USERS_LIST_CODE
    msg = msg.encode()
    print(msg.decode())
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(ans)
    return analysis.analysis_msg_main(ans)


def send_msg_handler(sock, msg_to_user, tar_username):
    # build protocol msg to sent a msg to spesific client
    username_len = str(len(tar_username))
    msg_to_user_len = str(len(msg_to_user))
    msg = analysis.GET + analysis.SEND_MSG_CODE + username_len.zfill(2) + tar_username + msg_to_user_len.zfill(
        2) + msg_to_user
    msg = msg.encode()
    print(msg.decode())

    # send it to server
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(analysis.analysis_msg_main(ans))


def send_msg_broadcast_handler(sock, msg_to_everyone):
    msg_to_everyone_len = str(len(msg_to_everyone))
    msg = analysis.GET + analysis.SEND_BROADCAST_MSG_CODE + msg_to_everyone_len.zfill(2) + msg_to_everyone
    msg = msg.encode()
    print(msg.decode())
    # send it to server
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    print(analysis.analysis_msg_main(ans))


def disconnect_handler(sock):
    msg = analysis.GET + analysis.DISCONNECT_CODE
    msg = msg.encode()
    sock.sendall(msg)
    ans = sock.recv(1024).decode()
    if analysis.analysis_msg_main(ans):
        sock.close()


def logic(option, sock, message=None, target=None, filename=None):
    if option is SEND_MSG_OPTION:
        send_msg_handler(sock, message, target)
    elif option is SEND_BROADCAST_MSG_OPTION:
        send_msg_broadcast_handler(sock, message)
    elif option is USERS_LIST_OPTION:
        return users_list_handler(sock)
    elif option is FILES_LIST_OPTION:
        return files_list_handler(sock)
    elif option is DOWNLOAD_OVER_UDP:
        return download_over_udp_handler(sock, filename)
    elif option is DOWNLOAD_OVER_TCP:
        return download_over_tcp_handler(sock, filename)
    else:
        disconnect_handler(sock)
