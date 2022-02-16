import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        #self.s = Server()

        self.assertEqual(True, True)

    def test_something(self):
        self.assertEqual(True, True)

    def test_analyse_data_by_protocol(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
