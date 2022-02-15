import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.assertEqual(True, True)

    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
