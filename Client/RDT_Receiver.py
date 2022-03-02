import socket

KB = 1024


class RDT_Receiver:
    # TODO: print logs for file textbox in GUI, get it from the constructor.
    def __init__(self, port, server_ip, filename):
        self.PORT = port
        self.FILENAME = filename
        self.file = open(f"./Downloaded_Files/{filename}", "wb")
        self.ADDRESS = (server_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.WINDOW_SIZE = 4
        self.last_is_order = False

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
        ack = 0
        self.sock.sendto("READY".encode(), self.ADDRESS)

        while not self.last_is_order:
            data, addr = self.sock.recvfrom(KB)
            is_last_packet, seq, application_data = self.analysis_data(data)

            if seq == ack:
                self.last_is_order = True if is_last_packet else False
                ack = self.calc_ack(seq)
                print("write to file..")
                print(is_last_packet, seq, application_data)
                self.file.write(application_data)
                packet_ack = self.build_ack_packet(ack)
                self.sock.sendto(packet_ack, self.ADDRESS)
            else:
                self.last_is_order = False
                print(is_last_packet, seq, application_data, "GET PACKET NOT IN ORDER!")

        self.file.close()
        self.sock.close()
        print("done")
