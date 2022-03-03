import socket
import os
import time
import tkinter
from tkinter import *

KB = 1024


class RDT_Receiver:
    # TODO: print logs for file textbox in GUI, get it from the constructor.
    def __init__(self, port, server_ip, filename, username, files_textbox, percentages_lbl, progress_bar, chat_window, FILE_SIZE):
        self.PORT = port
        self.FILENAME = filename
        if not os.path.isdir(f"./Downloaded_Files/{username}"):
            dirName = f"./Downloaded_Files/{username}"
            os.makedirs(dirName)

        self.file = open(f"./Downloaded_Files/{username}/{filename}", "wb")
        self.ADDRESS = (server_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.WINDOW_SIZE = 4
        self.last_is_order = False

        self.files_textbox = files_textbox
        self.chat_window = chat_window
        self.per_lbl = percentages_lbl
        self.prog_bar = progress_bar
        self.FILE_SIZE = int(FILE_SIZE)

    def analysis_data(self, data):
        is_last_packet = True if data[:1].decode() == '1' else False
        data = data[1:]
        seq = int(data[:1].decode())
        data = data[1:]
        application_data = data
        return is_last_packet, seq, application_data

    def calc_ack(self, seq):
        seq += 1
        seq %= self.WINDOW_SIZE
        return seq

    def build_ack_packet(self, ack):
        return str(ack).encode()

    def main(self):
        total_bytes = 0
        ack = 0
        i = 0
        self.sock.sendto("READY".encode(), self.ADDRESS)

        while not self.last_is_order:
            data, addr = self.sock.recvfrom(KB)
            is_last_packet, seq, application_data = self.analysis_data(data)

            #################
            i += 1
            if i % 5 == 0:
                continue
            #################

            if seq == ack:
                total_bytes += len(data)
                self.update_progress_bar(total_bytes, self.FILE_SIZE)
                print(total_bytes)
                self.last_is_order = True if is_last_packet else False
                ack = self.calc_ack(seq)
                print("write to file..")
                self.files_textbox.insert(END, f"write to file...\n")
                # print(is_last_packet, seq, application_data)
                self.file.write(application_data)
                packet_ack = self.build_ack_packet(ack)
                self.sock.sendto(packet_ack, self.ADDRESS)
                if is_last_packet:
                    self.files_textbox.insert(END, f"The last byte of the file is: {application_data[-1]}\n")
            else:
                self.last_is_order = False
                print("GET PACKET NOT IN ORDER!")
                self.files_textbox.insert(END, f"GET PACKET NOT IN ORDER!\n")

                # print(is_last_packet, seq, application_data, "GET PACKET NOT IN ORDER!")
        self.file.close()
        self.sock.close()
        print("done")

    def update_progress_bar(self, curr_bytes, total):
        self.chat_window.update_idletasks()
        curr_percentages = round((curr_bytes / total) * 100)
        print(curr_percentages)
        self.prog_bar['value'] = curr_percentages
        self.per_lbl['text'] = f"{self.prog_bar['value']}%"
