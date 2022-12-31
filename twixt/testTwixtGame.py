"""
Unit Tests for the TwixtGame class
"""
import unittest

from twixt.TwixtGame import TwixtGame

TEST_BOARD_SIZE = 12


class TestTwixtGame(unittest.TestCase):

    def setUp(self):
        self.game = TwixtGame(TEST_BOARD_SIZE)

    def test_get_board_size(self):
        current_board_size = self.game.getBoardSize()
        self.assertEqual(TEST_BOARD_SIZE, current_board_size)

    def test_get_init_board(self):
        initial_board = self.game.getInitBoard()
        self.assertIsNotNone(initial_board)


if __name__ == '__main__':
    unittest.main()
