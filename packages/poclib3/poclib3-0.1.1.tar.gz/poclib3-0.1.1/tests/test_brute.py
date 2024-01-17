import unittest
from poclib3.brute import WEAK_PASSWORD


class TestBruteWeakPassword(unittest.TestCase):

    def test_get_weak_password(self):
        self.assertTrue(len(WEAK_PASSWORD) > 0)


if __name__ == "__main__":
    unittest.main()
