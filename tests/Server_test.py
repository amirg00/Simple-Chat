import unittest
import sys


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

        self.assertEqual(True, True)

    def test_something(self):
        self.assertEqual(True, True)

    def test_analyse_data_by_protocol(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
