"""
Unit Tests for the TwixtGame class
"""
import unittest

from twixt.TwixtGame import TwixtGame
from twixt.TwixtBoard import *

TEST_BOARD_SIZE = 6


class TestTwixtGame(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_board_size(self):
        current_board_size = self.game.getBoardSize()
        self.assertEqual(TEST_BOARD_SIZE, current_board_size)

    def test_get_init_board(self):
        initial_board = self.game.getInitBoard()
        self.assertIsNotNone(initial_board)

    def test_display(self):
        board = TwixtBoard(10, 0)
        move1 = (3, 2)
        move2 = (4, 0)
        board.execute_move(move2, BLACK)
        board.execute_move(move1, RED)
        TwixtGame.display(board.board)


if __name__ == '__main__':
    unittest.main()
