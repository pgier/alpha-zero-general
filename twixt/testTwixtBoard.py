"""
Unit Tests for the TwixtBoard class
"""
import unittest

from TwixtBoard import TwixtBoard

RED = 1
BLACK = -1

SMALL_BOARD_SIZE = 6
SMALL_BOARD_TOTAL_LEGAL_MOVES = SMALL_BOARD_SIZE * SMALL_BOARD_SIZE


class TestTwixtBoard(unittest.TestCase):

    def setUp(self):
        pass

    def test_has_legal_moves(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        self.assertTrue(board.has_legal_moves())

    def test_get_legal_moves(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        legal_moves = board.get_legal_moves(RED)
        self.assertEqual(SMALL_BOARD_TOTAL_LEGAL_MOVES, len(legal_moves))

        center_move = (3, 4)
        board.execute_move(center_move, RED)
        legal_moves = board.get_legal_moves(BLACK)
        self.assertEqual(SMALL_BOARD_TOTAL_LEGAL_MOVES-1, len(legal_moves))

        board = TwixtBoard(SMALL_BOARD_SIZE)
        current_player = RED
        for x in range(board.n):
            for y in range(board.n):
                move = (x, y)
                board.execute_move(move, current_player)
                current_player *= -1
        legal_moves = board.get_legal_moves(current_player)
        self.assertEqual(0, len(legal_moves))


if __name__ == '__main__':
    unittest.main()
