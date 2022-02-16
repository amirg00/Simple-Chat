from enum import Enum


class Protocol(str, Enum):
    GET = "1"
    CONFIRM = "2"
    UPDATE = "3"
    ERROR = "4"

    CONNECT = "00"
    DISCONNECT = "01"
    USERS_LIST = "02"
    SEND_MESSAGE = "03"
    SEND_BROADCAST_MESSAGE = "04"
    FILES_LIST = "05"
    DOWNLOAD_FILE = "06"
