"""
Unit Tests for the TwixtBoard class
"""
import unittest

from twixt.TwixtBoard import TwixtBoard

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

    def test_twixt_links1(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        move_1 = (1, 1)
        board.execute_move(move_1, RED)
        move_2 = (2, 3)
        board.execute_move(move_2, RED)
        move_3 = (3, 5)
        board.execute_move(move_3, RED)
        move_4 = (1, 2)
        board.execute_move(move_4, BLACK)
        move_5 = (3, 3)
        board.execute_move(move_5, BLACK)
        self.assertEqual(3, len(board.linksRED))
        self.assertTrue(board.get_num(move_2) in board.get_links(move_1))
        self.assertTrue(board.get_num(move_3) in board.get_links(move_2))
        self.assertTrue(board.get_num(move_1) in board.get_links(move_2))
        self.assertFalse(board.get_num(move_3) in board.get_links(move_1))
        self.assertFalse(board.get_num(move_4) in board.get_links(move_5), "expected block by red")



if __name__ == '__main__':
    unittest.main()
