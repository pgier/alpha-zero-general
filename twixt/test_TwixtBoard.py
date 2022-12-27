import unittest

from twixt.TwixtBoard import TwixtBoard

TEST_BOARD_SIZE = 6


class TestTwixtBoard(unittest.TestCase):

    def setUp(self):
        self.board = TwixtBoard(TEST_BOARD_SIZE)

    def test_hasLegalMoves(self):
        self.assertTrue(True, self.board.has_legal_moves())


if __name__ == '__main__':
    unittest.main()
