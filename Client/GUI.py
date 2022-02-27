import threading
from threading import Thread
from tkinter import *
from tkinter import messagebox
import analysis_unit
import logic
import socket


class GUI:

    def __init__(self):
        self.send_server_sock = None
        self.chat_textBox = None
        self.users_menu = None
        self.users_var = None
        self.chat_online_users = []
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
                      font=('Helvetica', 13, 'bold'),
                      background="blue")
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
        canvas = Canvas(self.chat_window, width=750, height=500)
        canvas.pack()

        # Add lines in canvas widget
        canvas.create_line(0, 10, 375, 10, fill="black", width=2)
        canvas.create_line(375, 10, 375, 380, fill="black", width=2)
        canvas.create_line(0, 380, 375, 380, fill="black", width=2)
        canvas.create_line(3, 10, 3, 380, fill="black", width=2)

        text_chat = Text(self.chat_window,
                         # bg="#17202A",
                         # fg="#EAECEE",
                         font="Helvetica 10",
                         padx=1,
                         pady=1)
        text_chat.tag_configure('tag-center', justify='center')
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

        # choose list of the online clients.
        clicked = StringVar()
        users_menu = OptionMenu(self.chat_window,
                                clicked,
                                "everyone",
                                *self.chat_online_users)
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
        leave_button.place(x=0,
                           y=470,
                           height=30,
                           width=65)
        # Files buttons:
        select_file_button = Button(self.chat_window,
                                    text="Choose File",
                                    background="grey",
                                    height=2,
                                    width=8,
                                    cursor="hand2",
                                    command=lambda: self.select_file())
        select_file_button.bind("<Enter>", lambda e: select_file_button.config(bg='#929292'))
        select_file_button.bind("<Leave>", lambda e: select_file_button.config(bg='grey'))

        select_file_button.place(x=420,
                                 y=420,
                                 height=30,
                                 width=70)

        save_file_button = Button(self.chat_window,
                                  text="Save File",
                                  background="grey",
                                  height=2,
                                  width=8,
                                  cursor="hand2",
                                  command=lambda: self.save_file())
        save_file_button.bind("<Enter>", lambda e: save_file_button.config(bg='#929292'))
        save_file_button.bind("<Leave>", lambda e: save_file_button.config(bg='grey'))

        save_file_button.place(x=498,
                               y=420,
                               height=30,
                               width=65)

        select_protocol_button = Button(self.chat_window,
                                        text="protocol",
                                        background="grey",
                                        height=2,
                                        width=8,
                                        cursor="hand2",
                                        command=lambda: self.selected_protocol())
        select_protocol_button.bind("<Enter>", lambda e: select_protocol_button.config(bg='#929292'))
        select_protocol_button.bind("<Leave>", lambda e: select_protocol_button.config(bg='grey'))

        select_protocol_button.place(x=570,
                                     y=420,
                                     height=30,
                                     width=65)

        proceed_button = Button(self.chat_window,
                                text="Proceed",
                                background="grey",
                                height=2,
                                width=8,
                                cursor="hand2",
                                command=lambda: self.proceed())
        proceed_button.bind("<Enter>", lambda e: proceed_button.config(bg='#929292'))
        proceed_button.bind("<Leave>", lambda e: proceed_button.config(bg='grey'))

        proceed_button.place(x=640,
                             y=420,
                             height=30,
                             width=65)

        # labels:
        curr_user = Label(self.chat_window,
                          text="Me to: ",
                          font=('Helvetica', 12, 'bold'))
        curr_user.place(x=0, y=385)

    # -------------------------------------------------
    # ***************** Buttons Section ***************
    # -------------------------------------------------

    def leave_chat(self):
        user_response = messagebox.askyesnocancel("Leave Chat", "Are you sure you want to leave the chat?")
        if user_response is False or user_response is None:
            return
        logic.logic(logic.EXIT_OPTION, self.send_server_sock)
        self.chat_window.destroy()

    def send_button(self, client_message: Text, to="everyone"):
        client_send = threading.Thread(target=self.send_message, args=(client_message, to,))
        client_send.start()
        pass

    def send_message(self, client_message: Text, to="everyone"):
        client_msg = client_message.get(1.0, 'end-1c')
        if to == "everyone":
            self.chat_textBox.insert(END, f"Me to everyone: {client_msg}\n\n")
            choice = logic.SEND_BROADCAST_MSG_OPTION
            logic.logic(choice, self.send_server_sock, message=client_msg)
        else:
            self.chat_textBox.insert(END, f"Me to {to}: {client_msg}\n\n")
            logic.logic(logic.SEND_MSG_OPTION, self.send_server_sock, message=client_msg, target=to)
        client_message.delete('1.0', END)

    def connect_to_chat(self, SERVER_IP: str, SERVER_PORT: str, USERNAME: str):
        """
        The method connects the current user to the chat.
        :return: None
        """
        print(f"User: {USERNAME}, Server ip: {SERVER_IP}, Server port: {SERVER_PORT}")

        # see if the Entry fields are empty.
        if not SERVER_IP or not SERVER_PORT or not USERNAME:
            messagebox.showwarning("Empty Fields", "Please enter something in the detail fields!")
            return

        # Converting the string port to the real integer port number.
        server_port = int(SERVER_PORT)

        # connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (SERVER_IP, server_port)
        sock.connect(server_addr)
        self.chat_window.title(f"Chat Room - {USERNAME}")
        self.set_server_sock(sock)

        # enter to the chat as new friend inside
        port = self.log_in_to_chat(sock, USERNAME)
        if port == -1:
            return

        # listens for incoming messages from server.
        thread = Thread(target=self.listen_to_server, args=(port, SERVER_IP,))
        thread.start()

        # send a request for online users list:
        self.set_online_users_list(logic.logic(logic.USERS_LIST_OPTION, sock))
        print(self.chat_online_users)
        self.update_option_menu()

        self.connect_window.destroy()
        self.chat_window.deiconify()

    def exit(self):
        self.connect_window.destroy()

    def select_file(self):
        pass

    def save_file(self):
        pass

    def selected_protocol(self):
        pass

    def proceed(self):
        pass

    # ---------------------------------------------------------------
    # ***************** Auxiliary Methods For Buttons ***************
    # ---------------------------------------------------------------

    def log_in_to_chat(self, sock, username):
        print("user: " + username)
        is_log_in = False

        while is_log_in is not True:
            msg = "100" + str(len(username)).zfill(2) + username
            sock.sendall(msg.encode())
            ans = sock.recv(1024).decode()
            ans = analysis_unit.analysis_msg_main(ans)
            print(ans)
            print("------------------")
            if analysis_unit.ERROR in ans:
                code, type_code, type_error = ans
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

        username, port = ans
        print(f"Your username: {username} port for you: {port}")
        return port

    def listen_to_server(self, port, SERVER_IP):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = (SERVER_IP, port)
        sock.connect(server_addr)

        while True:
            msg = sock.recv(1024).decode()
            ans = analysis_unit.analysis_msg_main(msg)
            print(ans)
            print("------------------------")
            if analysis_unit.CONNECT_CODE in ans:
                type_code, username = ans
                self.center_label(self.chat_textBox,
                                  text=f"{username} has joined the chat",
                                  font='Arial 10 bold')
                self.chat_online_users.append(username)
                self.update_option_menu()
                print(self.chat_online_users)
                print(f"{username} added to chat")

            elif analysis_unit.DISCONNECT_CODE in ans:
                type_code, username = ans
                self.center_label(self.chat_textBox,
                                  text=f"{username} has left the chat",
                                  font='Arial 10 bold')
                print(self.chat_online_users)
                self.chat_online_users.remove(username)
                self.update_option_menu()
                print(f"{username} has left the chat")

            elif analysis_unit.SEND_MSG_CODE in ans:
                type_code, username, msg = ans
                self.chat_textBox.insert(END, f"{username} to you: {msg}\n\n")
                print(f"{username} to you: {msg}")

            elif analysis_unit.SEND_BROADCAST_MSG_CODE in ans:
                type_code, username, msg = ans
                self.chat_textBox.insert(END, f"{username} to everyone: {msg}\n\n")
                print(f"{username} to everyone: {msg}")
            else:
                pass

    def center_label(self, textbox, **kwargs):
        textbox.insert(END, ' ', 'tag-center')
        lbl = Label(textbox, bd=3, relief='solid', **kwargs, bg="#1ecbe1")
        textbox.window_create(END, window=lbl)
        textbox.insert(END, '\n\n')

    def update_online_user_list(self):
        logic.logic(logic.USERS_LIST_OPTION, self.send_server_sock)

    def update_option_menu(self):
        if not self.chat_online_users:
            return
        menu = self.users_menu["menu"]
        menu.delete(0, END)
        if "everyone" not in self.chat_online_users:
            self.chat_online_users.insert(0, "everyone")
        for user in self.chat_online_users:
            print(user)
            menu.add_command(label=user,
                             command=lambda value=user: self.users_var.set(value))


    def set_server_sock(self, sock):
        self.send_server_sock = sock

    def display_message(self):
        pass

    def set_chat_textBox(self, text: Text):
        self.chat_textBox = text

    def set_users_menu(self, users_menu):
        self.users_menu = users_menu

    def set_users_var(self, users_var):
        self.users_var = users_var

    def set_online_users_list(self, users_list: list):
        self.chat_online_users = users_list


if __name__ == "__main__":
    client = GUI()
