from enum import Enum
import socket


class Option(Enum):
    SEND = 1
    ACK_ARRIVED = 2
    TIMEOUT = 3
    # KiloByte is 1024 bytes
    KB = 1024


class RDT:
    def __init__(self, CLIENT_PORT, FILE_NAME):
        self.CLIENT_PORT = CLIENT_PORT
        self.FILE_NAME = FILE_NAME

        # opening the file, store data in the buffer.
        file = open(FILE_NAME, "br")
        self.BUFFER = file.read()
        file.close()

        self.window = []
        self.WINDOW_SIZE = 4
        self.PACKET_SIZE = 1000
        self.IP = "0.0.0.0"
        self.ADDRESS = (self.IP, CLIENT_PORT)
        self.ack = 0
        self.next_seq = 1
        self.can_window_slide = True
        self.last_packet_acked = False

    def build_packet(self):
        """create packet and save it in window
        packet view in window: (seq, b'XY<DATA>')
        so X is flag (1 or 0) indicate if this is the last
        packet, Y is seq and DATA is the application data.
        all of this saved in window as tuple of seq and packet."""

        is_last = 0 if len(self.BUFFER) > self.PACKET_SIZE else 1
        seq = str(0 if not self.window else (self.window[-1][0] + 1) % self.WINDOW_SIZE)
        application_data = self.BUFFER[:self.PACKET_SIZE]
        BUFFER = self.BUFFER[self.PACKET_SIZE:]
        packet = str(is_last).encode() + seq.encode() + application_data
        self.window.append((int(seq), packet))

    def send_packet(self, sock):
        """send all data in window to user"""
        seq, packet = self.window[-1]
        sock.sendto(packet, self.ADDRESS)

    def retransmition(self, sock):
        """send packet again"""
        for seq, packet in self.window:
            sock.sendto(packet, self.ADDRESS)

    def set_next_seq(self):
        """change status of next sequence that we want get in ack"""
        self.next_seq += 1
        self.next_seq %= self.WINDOW_SIZE

    def is_last_ack(self):
        """return True if the ACK was arrived is the last one (ack of last packet..)"""
        return True if not self.BUFFER and len(self.window) == 1 else False

    def go_back_n_loop(self, sock):
        """the main loop of GO-BACK-N"""
        while not self.last_packet_acked:
            if self.can_window_slide:
                self.go_back_n_options(Option.SEND, sock)
            else:
                try:

                    ack, addr = sock.recvfrom(Option.KB)
                    ack = int(ack.decode())
                    self.go_back_n_options(Option.ACK_ARRIVED, sock)
                except:
                    self.go_back_n_options(Option.TIMEOUT, sock)

    def go_back_n_options(self, case, sock):
        """
        The system have 3 options in the algorithm:
        1 - SEND THE NEXT packet in the buffer.
        2 - ACK WAS ARRIVED
            2.1 - ack is OK, it's what we have been waiting for
            OR
            2.2 - ack is NOT OK, it arrived after the allotted time for him to run out.
        3 - TIMEOUT: The waiting period for ACK has passed
        """
        if case == Option.SEND:
            # build packet, insert to the window and send it.
            self.build_packet()
            self.send_packet(sock)

            # stop fill the window if window is full
            window_can_slide = False if len(self.window) == self.WINDOW_SIZE else True

        elif case == Option.ACK_ARRIVED:
            if self.ack == self.next_seq:
                print(self.ack)
                # check if its last ack so can done.
                # if so, algorithm goes the end. and
                # we can sure that transfer is complete.
                if self.is_last_ack():
                    last_packet_acked = True

                # after ack was came, we know delete the
                # first packet in the window.
                # (this is the packet was acked!)
                # actualy, this is the silding(!)
                self.window.pop(0)

                # check if still have more data to sliding on it.
                # if no data-to-send was left outside the window,
                # so it's mean we get close to the end...
                window_can_slide = True if self.BUFFER else False

                # after we get the ack we was wainting for,
                # we waiting know to the next ack :)
                self.set_next_seq()
            else:
                print("lated ack!")

        elif case == Option.TIMEOUT:
            print("timeout!")

            # when TIMEOUT was happend, send
            # again all the packet inside the window.
            self.retransmition(sock)

        else:
            pass

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)  # set 2 seconds for wainting ack back

        # global DATA_TO_SEND
        # file_to_send = open("a.png", "br")
        # DATA_TO_SEND = file_to_send.read()
        # file_to_send.close()

        self.go_back_n_loop(sock)

        print("Sending is done")
        sock.close()

    if __name__ == "__main__":
        main()
