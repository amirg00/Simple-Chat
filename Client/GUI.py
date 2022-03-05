import threading
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox, _setit
from tkinter.ttk import Combobox, Progressbar
from tkinter import ttk

import analysis_unit
import logic
from RDT_Receiver import RDT_Receiver
import socket
import os


class GUI:

    def __init__(self):
        self.send_server_sock = None
        self.chat_textBox = None
        self.files_textBox = None
        self.transfer_progress_bar = None
        self.percentages = None
        self.users_menu = None
        self.users_var = None
        self.USERNAME = ""
        self.server_ip = None
        self.chat_online_users = []
        self.server_files = []
        self.chat_window = Tk()

        # hiding the chat window.
        self.chat_window.withdraw()
        self.set_chat_layout()

        # arranging connect window for the users.
        self.connect_window = Toplevel()
        self.set_entrance_layout()

        self.chat_window.mainloop()

    # --------------------------------------------------
    # ***************** Windows' Layouts ***************
    # --------------------------------------------------

    def set_entrance_layout(self) -> None:
        """
        The method sets the entrance window's layout, according to our design.
        :return: None
        """
        self.connect_window.geometry("500x500")
        self.connect_window.title("Chat")
        self.connect_window.resizable(width=False, height=False)

        # Create a canvas widget
        canvas = Canvas(self.connect_window, width=500, height=500)
        canvas.pack()

        # Add a line in canvas widget
        canvas.create_line(0, 30, 500, 30, fill="black", width=2)
        canvas.create_line(0, 70, 500, 70, fill="black", width=2)

        # entrance labels:
        label = Label(self.connect_window,
                      text="Fill up the address, port, and username,\n then click connect button.",
                      justify=CENTER,
                      font=('Helvetica', 13, 'bold'))
        # label.pack()
        label.place(x=90, y=150)

        address_label = Label(self.connect_window,
                              text='address: ',
                              font=('Helvetica', 10, 'bold'))
        address_label.place(x=0, y=0)

        port_label = Label(self.connect_window,
                           text='port: ',
                           font=('Helvetica', 10, 'bold'))
        port_label.place(x=260, y=0)

        username_label = Label(self.connect_window,
                               text='username: ',
                               font=('Helvetica', 10, 'bold'))
        username_label.place(x=0, y=40)

        # Entrance Entry fields:
        address = Entry(self.connect_window, bd=5)
        address.place(x=80, y=0)

        port = Entry(self.connect_window, bd=5)
        port.place(x=300, y=0)

        username = Entry(self.connect_window, bd=5)
        username.place(x=80, y=40)

        # Entrance buttons:
        connect_button = Button(self.connect_window,
                                text="Connect",
                                fg="white",
                                bg="#1b11ee",
                                font=('Helvetica', 13, 'bold'),
                                command=lambda: self.connect_to_chat(address.get(), port.get(), username.get()))

        connect_button.bind("<Enter>", lambda e: connect_button.config(fg='white', bg='#241bef', cursor="hand2"))
        connect_button.bind("<Leave>", lambda e: connect_button.config(fg='white', bg='#1b11ee', cursor="arrow"))
        connect_button.pack(side=LEFT)
        connect_button.place(x=185,
                             y=250,
                             height=40,
                             width=130)

        exit_button = Button(self.connect_window,
                             text="Exit",
                             background="red",
                             height=2,
                             width=8,
                             font=('Arial', 12, 'bold'),
                             command=lambda: self.exit())
        exit_button.bind("<Enter>", lambda e: exit_button.config(fg='white', bg='#ff2929', cursor="hand2"))
        exit_button.bind("<Leave>", lambda e: exit_button.config(fg='black', bg='red', cursor="arrow"))
        exit_button.pack()
        exit_button.place(x=-1, y=450)

    def set_chat_layout(self) -> None:
        self.chat_window.geometry("750x500")
        self.chat_window.title("Chat Room")
        self.chat_window.resizable(width=False, height=False)
        self.chat_window.configure(bg="#ACADA8")

        text_chat = Text(self.chat_window,
                         # bg="#ACADA8",
                         # fg="#EAECEE",
                         font="Helvetica 10",
                         padx=1,
                         pady=1,
                         state=DISABLED)
        text_chat.tag_configure('tag-center', justify='center')
        text_chat.tag_configure("bold", font="Helvetica 10 bold")

        text_chat.place(x=3,
                        y=11,
                        height=368,
                        width=370)
        self.set_chat_textBox(text_chat)

        # Scroll bar:
        scroll_bar = Scrollbar(text_chat)
        scroll_bar.place(relheight=1.01,
                         relx=0.965,
                         y=-1)
        # attach textbox to scrollbar
        text_chat.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=text_chat.yview, cursor="hand2")

        # Client's message box:
        client_msg = Text(self.chat_window,
                          # bg="#2C3E50",
                          # fg="#EAECEE",
                          font="Helvetica 10")
        client_msg.place(x=2,
                         y=420,
                         height=40,
                         width=320)

        # style for the OptionMenu:
        style = ttk.Style()
        style.configure("TMenubutton", background="#ACADA8", activebackground="#ACADA8")

        # choose list of the online clients.
        clicked = StringVar()
        users_menu = ttk.OptionMenu(self.chat_window,
                                    clicked,
                                    default="everyone",
                                    *self.chat_online_users,
                                    style="TMenubutton")
        users_menu.configure(cursor="hand2")

        users_menu.place(x=50,
                         y=385,
                         height=25,
                         width=95)
        self.set_users_menu(users_menu)
        self.set_users_var(clicked)

        # buttons:
        send_button = Button(self.chat_window,
                             text="Send",
                             background="blue",
                             foreground="white",
                             font=('Helvetica', 13, 'bold'),
                             height=2,
                             width=8,
                             cursor="hand2",
                             command=lambda: self.send_button(client_msg, to=clicked.get()))
        send_button.bind("<Enter>", lambda e: send_button.config(bg='#0d0dff', cursor="hand2"))
        send_button.bind("<Leave>", lambda e: send_button.config(bg='blue', cursor="arrow"))


        send_button.place(x=300,
                          y=420,
                          height=40,
                          width=60)

        leave_button = Button(self.chat_window,
                              text="Leave Chat",
                              background="red",
                              font=('Helvetica', 8, 'bold'),
                              height=2,
                              width=8,
                              command=lambda: self.leave_chat())
        leave_button.bind("<Enter>", lambda e: leave_button.config(fg='white', bg='#ff2929', cursor="hand2"))
        leave_button.bind("<Leave>", lambda e: leave_button.config(fg='black', bg='red', cursor="arrow"))
        leave_button.place(x=-1,
                           y=470,
                           height=30,
                           width=66)
        # Files buttons:
        # files combo-box:
        server_files = Combobox(self.chat_window,
                                state='readonly',
                                values=self.server_files,
                                postcommand=lambda: self.update_server_files(server_files))
        server_files.set("Choose a File")
        server_files.place(x=410,
                           y=10,
                           height=20,
                           width=300)

        download_button = Button(self.chat_window,
                                 text="Download",
                                 background="grey",
                                 height=2,
                                 width=8,
                                 cursor="hand2",
                                 command=lambda: self.download_file(server_files,
                                                                    protocol=("TCP" if choice.get() == 1 else "UDP")))
        download_button.bind("<Enter>", lambda e: download_button.config(bg='#929292'))
        download_button.bind("<Leave>", lambda e: download_button.config(bg='grey'))

        download_button.place(x=640,
                              y=420,
                              height=30,
                              width=65)
        # files text box:
        files_textBox = Text(self.chat_window,
                             # bg="#17202A",
                             # fg="#EAECEE",
                             font="Helvetica 10",
                             padx=1,
                             pady=1,
                             # state=DISABLED
                             )
        files_textBox.tag_configure('tag-center', justify='center')
        files_textBox.tag_config('warning', background="yellow", foreground="red", font=('Helvetica', 10, 'bold'))
        files_textBox.tag_config('success', background="#04fb54", font=('Helvetica', 10, 'bold'))
        files_textBox.tag_config('last-byte', foreground="#ed1253", font=('Helvetica', 10, 'bold'))
        files_textBox.tag_config('switch-protocol', foreground="#08f79e", font=('Helvetica', 10, 'bold'))
        files_textBox.tag_configure("bold", font="Helvetica 10 bold")

        files_textBox.place(x=410,
                            y=40,
                            height=330,
                            width=330)
        self.set_files_textBox(files_textBox)

        # Scroll bar:
        scroll_bar = Scrollbar(files_textBox)
        scroll_bar.place(relheight=1.01,
                         relx=0.960,
                         y=-1)
        # attach textbox to scrollbar
        files_textBox.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=files_textBox.yview, cursor="hand2")

        labelframe = LabelFrame(self.chat_window, text="Protocol", bg="#ACADA8")
        labelframe.pack()
        labelframe.place(x=420,
                         y=400,
                         height=70,
                         width=100)
        choice = IntVar()
        Radiobutton(labelframe,
                    text='TCP',
                    variable=choice,
                    value=1,
                    bg="#ACADA8",
                    activebackground="#ACADA8",
                    command=lambda: self.protocol_message_textbox(choice.get())).pack()
        Radiobutton(labelframe,
                    text='UDP',
                    variable=choice,
                    value=2,
                    bg="#ACADA8",
                    activebackground="#ACADA8",
                    command=lambda: self.protocol_message_textbox(choice.get())).pack()

        # labels:
        curr_user = Label(self.chat_window,
                          text="Me to: ",
                          font=('Helvetica', 12, 'bold'),
                          bg="#ACADA8")
        curr_user.place(x=0, y=385)

        # progress bar:
        progress_bar = Progressbar(self.chat_window,
                                   orient='horizontal',
                                   mode='determinate',
                                   length=280)
        self.set_progress_bar(progress_bar)
        progress_bar.place(x=420, y=375)
        self.percentages = Label(self.chat_window, text="%", bg="#ACADA8")
        self.percentages.place(x=705, y=375)

    # -------------------------------------------------
    # ***************** Buttons Section ***************
    # -------------------------------------------------

    def leave_chat(self) -> None:
        """
        The method is called when the leave chat button is pressed.
        Method first pops a pop-up window which asks the user to be sure that
        he wants leaving the chat, if so the method disconnects client following
        the protocol, and destroy the chat window. If not so, then method returns
        None to abort the leaving.
        :return: None
        """
        user_response = messagebox.askyesnocancel("Leave Chat", "Are you sure you want to leave the chat?")
        if user_response is False or user_response is None:
            return
        logic.logic(logic.EXIT_OPTION, self.send_server_sock)
        self.chat_window.destroy()

    def send_button(self, client_message: Text, to="everyone") -> None:
        """
        Method listening the send button in chat, such that when it is pressed the method runs automatically.
        This method built to run a new thread for client messages, because we want to enable the
        possibility to send and receive "in parallel".
        :param client_message: the client's message in Text type.
        :param to: target user the message is sent to.
        :return: None
        """
        client_send = threading.Thread(target=self.send_message, args=(client_message, to,))
        client_send.start()
        pass

    def send_message(self, client_message: Text, to="everyone") -> None:
        """
        Method sends the client's message to the target client ('to').
        If to is "everyone" it means we want to send a broadcast message for everyone in chat,
        following the protocol, except the sender. If 'to' is a specific user, then we send a
        message for the specific client following the protocol. Of course, we add to text
        box the current user's messages.
        :param client_message: the client's message in Text type.
        :param to: target user the message is sent to.
        :return: None
        """
        client_msg = client_message.get(1.0, 'end-1c')
        print("--------------")
        print("\t" in client_msg)
        print("--------------")
        if to == "everyone":
            self.chat_textBox.configure(state=NORMAL)
            self.chat_textBox.insert(END, f"Me to everyone:", "bold")
            self.chat_textBox.insert(END, f" {client_msg}\n\n")
            client_message.delete(1.0, END)
            self.chat_textBox.configure(state=DISABLED)
            self.chat_textBox.see(END)
            choice = logic.SEND_BROADCAST_MSG_OPTION
            logic.logic(choice, self.send_server_sock, message=client_msg)
        else:
            self.chat_textBox.configure(state=NORMAL)
            self.chat_textBox.insert(END, f"Me to {to}:", "bold")
            self.chat_textBox.insert(END, f" {client_msg}\n\n")
            client_message.delete(1.0, END)
            self.chat_textBox.configure(state=DISABLED)
            self.chat_textBox.see(END)
            logic.logic(logic.SEND_MSG_OPTION, self.send_server_sock, message=client_msg, target=to)

    def connect_to_chat(self, SERVER_IP: str, SERVER_PORT: str, USERNAME: str) -> None:
        """
        The method connects the current user to the chat.
        :return: None
        """
        print(f"User: {USERNAME}, Server ip: {SERVER_IP}, Server port: {SERVER_PORT}")

        # see if the Entry fields are empty.
        if not SERVER_IP or not SERVER_PORT or not USERNAME:
            messagebox.showwarning("Empty Fields", "Please enter something in the detail fields!")
            return

        # set server ip property
        self.set_server_ip(SERVER_IP)

        # set client's username property
        self.set_username(USERNAME)

        # Converting the string port to the real integer port number.
        if not SERVER_PORT.isnumeric() or int(SERVER_PORT) != 13337:
            messagebox.showerror("Port Incorrect", "Error: port has to be 13337.")
            return
        server_port = int(SERVER_PORT)

        # connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (SERVER_IP, server_port)
        try:
            sock.connect(server_addr)
        except:
            messagebox.showerror("Connection ERROR", "ERROR - Details aren't correct, or server isn't up."
                                                     "\nPlease try again later, "
                                                     "and make sure your IP is correct.")
            return
        self.chat_window.title(f"Chat Room - {USERNAME}")
        self.set_server_sock(sock)

        # enter to the chat as new friend inside
        port = self.log_in_to_chat(sock, USERNAME)
        if port == -1:
            return

        # listens for incoming messages from server with thread attached to method.
        thread = Thread(target=self.listen_to_server, args=(port, SERVER_IP,))
        thread.start()

        # send a request for online users list:
        self.set_online_users_list(logic.logic(logic.USERS_LIST_OPTION, sock))
        print(self.chat_online_users)
        self.update_option_menu()

        self.connect_window.destroy()
        self.chat_window.deiconify()
        self.center_label(self.chat_textBox,
                          text=f"you have joined the chat",
                          font='Arial 10 bold')

    def exit(self) -> None:
        """
        Method exits from connect window, after the exit button is pressed.
        :return: None
        """
        self.connect_window.destroy()

    def download_file(self, server_files_combobox: Combobox, protocol=None):
        """
        This method downloads the file by the given protocol.
        :param server_files_combobox: the ref of the files combobox.
        :param protocol: preferred download protocol.
        :return:
        """
        print(protocol)
        FILENAME = server_files_combobox.get()
        print(FILENAME)
        if FILENAME == "Choose a File":
            messagebox.showerror("File Not Found", "You haven't chosen a file.\nPlease choose a file.")
            return
        if protocol == "UDP":
            port, FILE_SIZE = logic.logic(option=logic.DOWNLOAD_OVER_UDP, sock=self.send_server_sock, filename=FILENAME)
            rdt = RDT_Receiver(port, self.server_ip, FILENAME, self.USERNAME, self.files_textBox, self.percentages,
                               self.transfer_progress_bar, self.chat_window, FILE_SIZE)
            download_thread_over_udp = Thread(target=rdt.main, args=())
            download_thread_over_udp.start()
        else:
            port, FILE_SIZE = logic.logic(option=logic.DOWNLOAD_OVER_TCP, sock=self.send_server_sock, filename=FILENAME)
            receive_thread = Thread(target=self.receive_file_by_TCP, args=(port, FILENAME, FILE_SIZE,))
            receive_thread.start()

    # ---------------------------------------------------------------
    # ***************** Auxiliary Methods For Buttons ***************
    # ---------------------------------------------------------------

    def receive_file_by_TCP(self, PORT, FILENAME, FILE_SIZE):
        # connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (self.server_ip, PORT)
        sock.connect(server_addr)
        KB = 1024
        total_bytes = 0
        if not os.path.isdir(f"./Downloaded_Files/{self.USERNAME}"):
            dirName = f"./Downloaded_Files/{self.USERNAME}"
            os.makedirs(dirName)

        with open(f"./Downloaded_Files/{self.USERNAME}/{FILENAME}", "wb") as file:
            while True:
                receive_bytes = sock.recv(KB)
                # print(len(receive_bytes))
                total_bytes += len(receive_bytes)
                self.update_progress_bar(total_bytes, int(FILE_SIZE))
                if not receive_bytes:
                    break
                file.write(receive_bytes)

        file.close()
        sock.close()

    def update_progress_bar(self, curr_bytes, total):
        self.chat_window.update_idletasks()
        curr_percentages = round((curr_bytes / total) * 100)
        print(curr_percentages)
        self.transfer_progress_bar['value'] = curr_percentages
        self.percentages['text'] = f"{self.transfer_progress_bar['value']}%"

    def log_in_to_chat(self, sock, username) -> int:
        """
        Method connects the username to the chat following the protocol,
        if an error response from the server is returned (following the protocol), it pops a pop-up window,
        to let user know with the error/warning specified in the pop-up window.
        If there isn't an error found, we get the port allocated by the server from
        analyzing the server's response.
        :param sock: a reference to the username's send socket.
        :param username: a given username.
        :return: new port allocated by the server (could be in range -> (55000, 55015)) for the new listening socket.
        """
        print("user: " + username)
        is_log_in = False

        while is_log_in is not True:
            msg = "100" + str(len(username)).zfill(2) + username
            sock.sendall(msg.encode())
            res = sock.recv(1024).decode()
            res = analysis_unit.analysis_msg_main(res)
            print(res)
            print("------------------")
            if analysis_unit.ERROR in res:
                code, type_code, type_error = res
                print(type_code)
                if type_error == "1":
                    messagebox.showwarning("Invalid Username", "Please enter a valid username.")
                    return -1
                    print("Invalid username! try again.")

                elif type_error == "2":
                    messagebox.showerror("Username Taken", "Error 4002 - This username is already taken.\nPlease "
                                                           "choose another name or try later.")
                    print("Username was taken! try again.")
                    return -1

                elif type_error == "3":
                    messagebox.showerror("Connection Failed", "Error 4003 - Server is full.\nPlease try later.")
                    print("Server full.. try later.")
                    sock.close()
                    exit()
                else:
                    pass
            else:
                is_log_in = True

        username, port = res
        print(f"Your username: {username} port for you: {port}")
        return port

    def listen_to_server(self, port, SERVER_IP) -> None:
        """
        This method is a client's thread listening to server.
        In this method we listen to the income (30X - broadcast) messages from the server,
        with an infinite loop, with the port allocated by server earlier (55000-55015).
        :param port: a given port to listen for incoming messages from server.
        :param SERVER_IP: a given server's ip.
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (SERVER_IP, port)
        sock.connect(server_addr)

        while True:
            msg = sock.recv(1024).decode()
            res = analysis_unit.analysis_msg_main(msg)
            # print(res)
            # print("------------------------")
            if analysis_unit.CONNECT_CODE in res:
                type_code, username = res
                self.center_label(self.chat_textBox,
                                  text=f"{username} has joined the chat",
                                  font='Arial 10 bold')
                self.chat_online_users.append(username)
                self.update_option_menu()
                # print(self.chat_online_users)
                # print(f"{username} added to chat")

            elif analysis_unit.DISCONNECT_CODE in res:
                type_code, username = res
                self.center_label(self.chat_textBox,
                                  text=f"{username} has left the chat",
                                  font='Arial 10 bold')
                # print(self.chat_online_users)
                self.chat_online_users.remove(username)
                self.update_option_menu()
                # print(f"{username} has left the chat")

            elif analysis_unit.SEND_MSG_CODE in res:
                type_code, username, msg = res
                self.chat_textBox.configure(state=NORMAL)
                self.chat_textBox.insert(END, f"{username} to you:", "bold")
                self.chat_textBox.insert(END, f" {msg}\n\n")
                self.chat_textBox.configure(state=DISABLED)
                self.chat_textBox.see(END)
                # print(f"{username} to you: {msg}")

            elif analysis_unit.SEND_BROADCAST_MSG_CODE in res:
                type_code, username, msg = res
                self.chat_textBox.configure(state=NORMAL)
                self.chat_textBox.insert(END, f"{username} to everyone:", "bold")
                self.chat_textBox.insert(END, f" {msg}\n\n")
                self.chat_textBox.configure(state=DISABLED)
                self.chat_textBox.see(END)
                # print(f"{username} to everyone: {msg}")

    def protocol_message_textbox(self, choice) -> None:
        """
        This method gets the preferred protocol by the user,
        and then insert logs for that.
        :param choice: the choice of tcp or udp
        :return: None
        """
        print(choice)
        self.files_textBox.configure(state=NORMAL)
        if choice == 1:
            self.files_textBox.insert(END, f"Download protocol has set to TCP\n", "bold")
        else:
            self.files_textBox.insert(END, f"Download protocol has set to UDP\n", "bold")
        self.files_textBox.configure(state=DISABLED)
        self.files_textBox.see(END)

    def center_label(self, textbox, **kwargs) -> None:
        """
        Method created a decorated box for leaving and joining messages,
        which will be centered at the center within the chat's text box, after inserting
        the decorated label to the text box.
        :param textbox: user's chat text box.
        :param kwargs: more values...
        :return: None
        """
        textbox.configure(state=NORMAL)
        textbox.insert(END, ' ', 'tag-center')
        lbl = Label(textbox, bd=3, relief='solid', **kwargs, bg="#1ecbe1")
        textbox.window_create(END, window=lbl)
        textbox.insert(END, '\n\n')
        textbox.configure(state=DISABLED)
        textbox.see(END)

    def update_online_user_list(self):
        logic.logic(logic.USERS_LIST_OPTION, self.send_server_sock)

    def update_option_menu(self):
        """
        This method updates a certain option menu, in our case,
        it updates the online users list (list of all users connected except current user),
        after somebody leaves/joins the chat.
        :return:
        """
        if not self.chat_online_users:
            return
        menu = self.users_menu["menu"]
        menu.delete(0, END)
        if "everyone" not in self.chat_online_users:
            self.chat_online_users.insert(0, "everyone")
        for user in self.chat_online_users:
            print(user)
            menu.add_radiobutton(label=user,
                                 command=_setit(self.users_var, user))

    def update_server_files(self, files_combobox: Combobox):
        files = logic.logic(logic.FILES_LIST_OPTION, self.send_server_sock)
        print(files)
        self.set_server_files(files)
        files_combobox.config(values=self.server_files)

    # ---------------------------------------------------------------
    # ************************  Set Methods *************************
    # ---------------------------------------------------------------

    def set_server_sock(self, sock) -> None:
        """
        The method sets the socket property of the class, to be the given socket.
        :param sock: a given socket.
        :return: None
        """
        self.send_server_sock = sock

    def set_chat_textBox(self, text: Text) -> None:
        """
        Method sets the chat's text-box property to be the given textbox.
        :param text: a given text-box.
        :return: None
        """
        self.chat_textBox = text

    def set_users_menu(self, users_menu) -> None:
        """
        Method sets users menu property by a given user menu.
        :param users_menu: a given users menu.
        :return: None
        """
        self.users_menu = users_menu

    def set_users_var(self, users_var) -> None:
        self.users_var = users_var

    def set_online_users_list(self, users_list: list) -> None:
        self.chat_online_users = users_list

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def set_server_files(self, server_files):
        self.server_files = server_files

    def set_files_textBox(self, textBox: Text):
        self.files_textBox = textBox

    def set_username(self, username):
        self.USERNAME = username

    def set_progress_bar(self, progress_bar):
        self.transfer_progress_bar = progress_bar


if __name__ == "__main__":
    client = GUI()
