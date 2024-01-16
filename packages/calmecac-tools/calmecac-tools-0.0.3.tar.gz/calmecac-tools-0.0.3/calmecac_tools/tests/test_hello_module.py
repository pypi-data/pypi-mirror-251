import unittest
from calmecac_tools import hello_module


class TestHello(unittest.TestCase):
    def test_say_hello(self):
        self.assertEqual(hello_module.say_hello(), "Hello from calmecac-tools!")


if __name__ == "__main__":
    unittest.main()
