import socket
import os
import time
import tkinter
from tkinter import *
from tkinter import messagebox


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
        self.WINDOW_SIZE = 20+1
        self.last_is_order = False

        self.files_textbox = files_textbox
        self.chat_window = chat_window
        self.per_lbl = percentages_lbl
        self.prog_bar = progress_bar
        self.FILE_SIZE = int(FILE_SIZE)

    def analysis_data(self, data):
        is_last_packet = True if data[:1].decode() == '1' else False
        data = data[1:]
        seq = int(data[:2].decode())
        data = data[2:]
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
        self.sock.sendto("20".encode(), self.ADDRESS)

        while not self.last_is_order:
            data, addr = self.sock.recvfrom(KB)
            is_last_packet, seq, application_data = self.analysis_data(data)

            #################
            i += 1
            if i % 10 == 0:
                time.sleep(2)
            if i % 11 == 0:
                continue
            #################

            if seq == ack:
                total_bytes += len(data)
                self.update_progress_bar(total_bytes, self.FILE_SIZE)
                print(total_bytes)
                self.last_is_order = True if is_last_packet else False
                ack = self.calc_ack(seq)
                print("write to file..")
                self.files_textbox.configure(state=NORMAL)
                self.files_textbox.insert(END, f"Writing to file...\n", "bold")
                self.files_textbox.configure(state=DISABLED)
                self.files_textbox.see(END)
                self.file.write(application_data)
                packet_ack = self.build_ack_packet(ack)
                self.sock.sendto(packet_ack, self.ADDRESS)
                if is_last_packet:

                    self.files_textbox.configure(state=NORMAL)
                    self.files_textbox.insert(END, f"Last byte of the file is: ", "bold")
                    self.files_textbox.insert(END, f"{application_data[-1]}\n", "last-byte")

                    self.files_textbox.configure(state=DISABLED)
                    self.files_textbox.see(END)
            else:
                self.sock.sendto(packet_ack, self.ADDRESS) # try to lated acks
                self.last_is_order = False
                print("GET PACKET NOT IN ORDER!")
                self.files_textbox.configure(state=NORMAL)
                self.files_textbox.insert(END, f"GOT PACKET NOT IN ORDER!\n", 'warning')
                self.files_textbox.configure(state=DISABLED)
                self.files_textbox.see(END)
                # print(is_last_packet, seq, application_data, "GET PACKET NOT IN ORDER!")
        self.file.close()
        self.sock.close()
        self.files_textbox.configure(state=NORMAL)
        self.files_textbox.insert(END, f"File has downloaded successfully!!!\n", 'success')
        self.files_textbox.configure(state=DISABLED)
        self.files_textbox.see(END)

        print("done")

    def update_progress_bar(self, curr_bytes, total) -> None:
        """
        The method updates the progress bar by the packets.
        :param curr_bytes: current total bytes downloaded from file.
        :param total: the total file size.
        :return: None
        """
        self.chat_window.update_idletasks()
        curr_percentages = round((curr_bytes / total) * 100)
        self.prog_bar['value'] = curr_percentages
        self.per_lbl['text'] = f"{self.prog_bar['value']}%"
