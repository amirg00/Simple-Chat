import unittest
from .. import analysis_unit


class MyTestCase(unittest.TestCase):
    Description = """ 
                  Here we will examine any possible response from server,
                  for some inputted ports and usernames. This will resemble
                  a working running server which responses to chat's users requests.
                  """

    def setUp(self) -> None:
        self.chat_ports   = [55000, 55001, 55002, 55003, 55004]
        self.files_ports  = [55006, 55007, 55008]
        self.server_files = ["a.txt", "b.png", "c.txt"]
        self.files_size   = ["30", "120", "5"]
        # Suppose these next users are connected to chat.
        self.users = ["amirg",
                      "123as",
                      "ALICE",
                      "BOB",
                      "AA"]
        # For testing users list:
        self.connected_users_list = [["amirg"], ["123as"], ["ALICE"], ["BOB"], ["AA"],
                                     ["amirg", "123as"], ["123as", "ALICE"], ["ALICE", "BOB"],
                                     ["BOB", "AA"], ["AA", "amirg"], ["amirg", "123as", "ALICE"],
                                     ["123as", "ALICE", "BOB"], ["ALICE", "BOB", "AA"],
                                     ["amirg", "123as", "ALICE", "BOB"], ["123as", "ALICE", "BOB", "AA"]]

        self.messages = ["blabla", "12345", "", "blabla\nblablablabla", "blabla\nblabla\n"]

        # --------------------------------------------------------------------------- #
        # *********** Response (200) Messages - Client Analysis ********************* #
        # ----------------------------------------------------------------------------#
        self.messages_200 = [
            # --------- Connect To Server (200) messages ----------- #
            f"{200}05{self.users[0]}{self.chat_ports[0]}",
            f"{200}05{self.users[1]}{self.chat_ports[1]}",
            f"{200}05{self.users[2]}{self.chat_ports[2]}",
            f"{200}03{self.users[3]}{self.chat_ports[3]}",
            f"{200}02{self.users[4]}{self.chat_ports[4]}",

            # --------- Disconnect (201) Messages ----------- #
            f"{201}",

            # --------- Users List (202) Messages ----------- #
            # Examine cases for message 202 where only some users are connected to chat.
            f"{202}{0}",  # Nobody is connected except current user.

            # Cases (5) in which only one user is connected except current user:
            f"{202}{1}{1}{str(len(self.users[0])).zfill(2)}{self.users[0]}",
            f"{202}{1}{1}{str(len(self.users[1])).zfill(2)}{self.users[1]}",
            f"{202}{1}{1}{str(len(self.users[2])).zfill(2)}{self.users[2]}",
            f"{202}{1}{1}{str(len(self.users[3])).zfill(2)}{self.users[3]}",
            f"{202}{1}{1}{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # Cases (5) in which there are two users that connected, except current user:
            f"{202}{1}{2}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}",

            f"{202}{1}{2}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}",

            f"{202}{1}{2}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{202}{1}{2}{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            f"{202}{1}{2}{str(len(self.users[4])).zfill(2)}{self.users[4]}"
            f"{str(len(self.users[0])).zfill(2)}{self.users[0]}",

            # Cases (3) in which there are three users that connected, except current user:
            f"{202}{1}{3}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}",

            f"{202}{1}{3}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{202}{1}{3}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # Cases (2) in which all four users are connected, except current user:
            f"{202}{1}{4}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{202}{1}{4}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # --------- 203 Messages - Confirm PRIVATE Message ----------- #
            f"{203}",
            # --------- 204 Messages - Confirm Broadcast Message ----------- #
            # Examine cases for message 202 where only some users are connected to chat.
            f"{204}{0}",  # Nobody is connected except current user.

            # Cases (5) in which only one user is connected except current user:
            f"{204}{1}{1}{str(len(self.users[0])).zfill(2)}{self.users[0]}",
            f"{204}{1}{1}{str(len(self.users[1])).zfill(2)}{self.users[1]}",
            f"{204}{1}{1}{str(len(self.users[2])).zfill(2)}{self.users[2]}",
            f"{204}{1}{1}{str(len(self.users[3])).zfill(2)}{self.users[3]}",
            f"{204}{1}{1}{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # Cases (5) in which there are two users that connected, except current user:
            f"{204}{1}{2}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}",

            f"{204}{1}{2}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}",

            f"{204}{1}{2}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{204}{1}{2}{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            f"{204}{1}{2}{str(len(self.users[4])).zfill(2)}{self.users[4]}"
            f"{str(len(self.users[0])).zfill(2)}{self.users[0]}",

            # Cases (3) in which there are three users that connected, except current user:
            f"{204}{1}{3}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}",

            f"{204}{1}{3}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{204}{1}{3}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # Cases (2) in which all four users are connected, except current user:
            f"{204}{1}{4}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}",

            f"{204}{1}{4}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # --------- Files List (205) Message ----------- #

            # when a server doesn't have files:

            f"{205}{0}",

            # all three server's files:
            f"{205}{1}03{str(len(self.server_files[0])).zfill(2)}{self.server_files[0]}"
            f"{str(len(self.server_files[1])).zfill(2)}{self.server_files[1]}"
            f"{str(len(self.server_files[2])).zfill(2)}{self.server_files[2]}",

            # --------- Files List (206) Message ----------- #

            # User has requested the a.txt file whose size is 30 bytes:
            f"{206}02{30}{self.files_ports[0]}",
            # User has requested the b.png file whose size is 120 bytes:
            f"{206}03{120}{self.files_ports[1]}",
            # User has requested the c.txt file whose size is 5 bytes:
            f"{206}01{5}{self.files_ports[2]}"
        ]

        # --------------------------------------------------------------------------- #
        # *********** Response (300) Messages - Client Analysis ********************* #
        # ----------------------------------------------------------------------------#
        self.messages_300 = [

            # --------- Client Connected (300) Message ----------- #
            f"{300}{str(len(self.users[0])).zfill(2)}{self.users[0]}",
            f"{300}{str(len(self.users[1])).zfill(2)}{self.users[1]}",
            f"{300}{str(len(self.users[2])).zfill(2)}{self.users[2]}",
            f"{300}{str(len(self.users[3])).zfill(2)}{self.users[3]}",
            f"{300}{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # --------- Client Disconnected (301) Message ----------- #
            f"{301}{str(len(self.users[0])).zfill(2)}{self.users[0]}",
            f"{301}{str(len(self.users[1])).zfill(2)}{self.users[1]}",
            f"{301}{str(len(self.users[2])).zfill(2)}{self.users[2]}",
            f"{301}{str(len(self.users[3])).zfill(2)}{self.users[3]}",
            f"{301}{str(len(self.users[4])).zfill(2)}{self.users[4]}",

            # --------- Private (303) Message ----------- #
            f"{303}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.messages[0])).zfill(2)}{self.messages[0]}",

            f"{303}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.messages[1])).zfill(2)}{self.messages[1]}",

            f"{303}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.messages[2])).zfill(2)}{self.messages[2]}",

            f"{303}{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.messages[3])).zfill(2)}{self.messages[3]}",

            f"{303}{str(len(self.users[4])).zfill(2)}{self.users[4]}"
            f"{str(len(self.messages[4])).zfill(2)}{self.messages[4]}",
            
            # --------- Broadcast (304) Message ----------- #
            f"{304}{str(len(self.users[0])).zfill(2)}{self.users[0]}"
            f"{str(len(self.messages[0])).zfill(2)}{self.messages[0]}",

            f"{304}{str(len(self.users[1])).zfill(2)}{self.users[1]}"
            f"{str(len(self.messages[1])).zfill(2)}{self.messages[1]}",

            f"{304}{str(len(self.users[2])).zfill(2)}{self.users[2]}"
            f"{str(len(self.messages[2])).zfill(2)}{self.messages[2]}",

            f"{304}{str(len(self.users[3])).zfill(2)}{self.users[3]}"
            f"{str(len(self.messages[3])).zfill(2)}{self.messages[3]}",

            f"{304}{str(len(self.users[4])).zfill(2)}{self.users[4]}"
            f"{str(len(self.messages[4])).zfill(2)}{self.messages[4]}"
        ]

        # --------------------------------------------------------------------------- #
        # *********** Response (400) Messages - Client Analysis ********************* #
        # ----------------------------------------------------------------------------#

        self.messages_400 = [

            # --------- Connection Issue (400X) Message ----------- #
            f"{400}{1}",  # Username isn't valid
            f"{400}{2}",  # Username is taken
            f"{400}{3}",  # Server is full.

            # --------- Sending Message Issue (403X) Message ----------- #
            f"{403}{1}",  # Target username doesn't exist.

            # --------- Sending File Issue (406X) Message ----------- #
            f"{406}{1}"  # Requested file doesn't exist on server.
        ]

    def test_analysis_confirms_msg(self):
        """This method tests 200 messages."""

        user_cnt = 0
        users_list_cnt = 0
        broadcast_cnt = 0
        files_cnt = 0

        for server_res in self.messages_200:
            if server_res.startswith("200"):
                self.assertEqual(analysis_unit.analysis_confirms_msg(analysis_unit.CONNECT_CODE, server_res[3:]),
                                 (self.users[user_cnt], self.chat_ports[user_cnt]))
                user_cnt += 1

            elif server_res.startswith("201"):
                self.assertTrue(analysis_unit.analysis_confirms_msg(analysis_unit.DISCONNECT_CODE, server_res))

            elif server_res.startswith("202"):
                connected_users = analysis_unit.analysis_confirms_msg(analysis_unit.USERS_LIST_CODE, server_res[3:])
                if server_res.startswith("2020"):
                    self.assertEqual(connected_users, [])
                    continue
                self.assertEqual(connected_users, self.connected_users_list[users_list_cnt])
                users_list_cnt += 1

            elif server_res.startswith("203"):
                self.assertTrue(analysis_unit.analysis_confirms_msg(analysis_unit.SEND_MSG_CODE, server_res[3:]))

            elif server_res.startswith("204"):
                connected_users = analysis_unit.analysis_confirms_msg(analysis_unit.SEND_BROADCAST_MSG_CODE,
                                                                      server_res[3:])
                if server_res.startswith("2040"):
                    self.assertEqual(connected_users, [])
                    continue
                self.assertEqual(connected_users, self.connected_users_list[broadcast_cnt])
                broadcast_cnt += 1

            elif server_res.startswith("205"):
                if server_res == "2050":
                    self.assertEqual(analysis_unit.analysis_confirms_msg(analysis_unit.FILES_LIST_CODE, server_res[3:]),
                                     [])
                    continue
                self.assertEqual(analysis_unit.analysis_confirms_msg(analysis_unit.FILES_LIST_CODE, server_res[3:]),
                                 self.server_files)

            elif server_res.startswith("206"):
                self.assertEqual(analysis_unit.analysis_confirms_msg(analysis_unit.DOWNLOAD_FILE, server_res[3:]),
                                 (self.files_ports[files_cnt], self.files_size[files_cnt]))
                files_cnt += 1

    def test_analysis_updates_msg(self):
        """This method tests 300 messages."""

        user_connect_cnt = 0
        user_disconnect_cnt = 0
        private_msg_cnt = 0
        broadcast_msg_cnt = 0
        for server_res in self.messages_300:
            if server_res.startswith("300"):
                self.assertEqual(analysis_unit.analysis_updates_msg(analysis_unit.CONNECT_CODE, server_res[3:]),
                                 (analysis_unit.CONNECT_CODE, self.users[user_connect_cnt]))
                user_connect_cnt += 1

            elif server_res.startswith("301"):
                print(user_disconnect_cnt)
                print(server_res)
                self.assertEqual(analysis_unit.analysis_updates_msg(analysis_unit.DISCONNECT_CODE, server_res[3:]),
                                 (analysis_unit.DISCONNECT_CODE, self.users[user_disconnect_cnt]))
                user_disconnect_cnt += 1

            elif server_res.startswith("303"):
                self.assertEqual(analysis_unit.analysis_updates_msg(analysis_unit.SEND_MSG_CODE, server_res[3:]),
                            (analysis_unit.SEND_MSG_CODE, self.users[private_msg_cnt], self.messages[private_msg_cnt]))
                private_msg_cnt += 1

            elif server_res.startswith("304"):
                self.assertEqual(analysis_unit.analysis_updates_msg(analysis_unit.SEND_BROADCAST_MSG_CODE, server_res[3:]),
                                 (analysis_unit.SEND_BROADCAST_MSG_CODE, self.users[broadcast_msg_cnt],
                                  self.messages[broadcast_msg_cnt]))
                broadcast_msg_cnt += 1

    def test_analysis_errors_msg(self):
        """This method tests 400 messages."""
        for server_res in self.messages_400:
            if server_res.startswith("400"):
                self.assertEqual(analysis_unit.analysis_errors_msg("00", server_res[3:]),
                                 (analysis_unit.ERROR, "00", server_res[3:]))
            elif server_res.startswith("403"):
                self.assertEqual(analysis_unit.analysis_errors_msg("03", server_res[3:]),
                                 (analysis_unit.ERROR, "03", server_res[3:]))

            elif server_res.startswith("406"):
                self.assertEqual(analysis_unit.analysis_errors_msg("06", server_res[3:]),
                                 (analysis_unit.ERROR, "06", server_res[3:]))


if __name__ == '__main__':
    unittest.main()
