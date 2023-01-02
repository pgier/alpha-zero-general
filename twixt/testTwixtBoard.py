"""
Unit Tests for the TwixtBoard class
"""
import random
import unittest

from twixt.TwixtBoard import *


SMALL_BOARD_SIZE = 6
SMALL_BOARD_TOTAL_LEGAL_MOVES = SMALL_BOARD_SIZE * SMALL_BOARD_SIZE


class TestTwixtBoard(unittest.TestCase):

    def setUp(self):
        pass

    def test_board_index(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        x = 2
        y = 3
        self.assertEqual(EMPTY, board[x][y])
        move = (x, y)
        board.execute_move(move, RED)
        self.assertEqual(RED, board[x][y], "expected red, found {0}".format(color_name[board[x][y]]))

    def test_board_get(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        pos = (2, 3)
        self.assertEqual(EMPTY, board.get_pos(pos))
        board.execute_move(pos, RED)
        self.assertEqual(RED, board.get_pos(pos), "expected red, found {0}".format(color_name[board.get_pos(pos)]))

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
        self.assertEqual(SMALL_BOARD_TOTAL_LEGAL_MOVES - 1, len(legal_moves))

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
        move_3 = (4, 2)
        board.execute_move(move_3, RED)
        self.assertEqual(3, len(board.links_red))
        self.assertTrue(move_2 in board.get_links(move_1))
        self.assertTrue(move_3 in board.get_links(move_2))
        self.assertTrue(move_1 in board.get_links(move_2))
        self.assertFalse(move_3 in board.get_links(move_1))
        move_4 = (1, 2)
        board.execute_move(move_4, BLACK)
        move_5 = (3, 1)
        board.execute_move(move_5, BLACK)
        self.assertFalse(move_4 in board.get_links(move_5), "expected block by red")

    def test_twixt_links2(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        move_1 = (1, 1)
        board.execute_move(move_1, RED)
        move_2 = (3, 2)
        board.execute_move(move_2, BLACK)
        move_3 = (2, 3)
        board.execute_move(move_3, RED)
        move_4 = (5, 3)
        board.execute_move(move_4, BLACK)
        move_5 = (4, 2)
        board.execute_move(move_5, RED)
        move_6 = (3, 4)
        board.execute_move(move_6, BLACK)
        move_7 = (0, 1)
        board.execute_move(move_7, RED)
        move_8 = (1, 3)
        board.execute_move(move_8, RED)
        self.assertFalse(move_6 in board.get_links(move_3))
        self.assertTrue(move_8 in board.get_links(move_7))
        self.assertFalse(move_5 in board.get_links(move_3))

    def test_is_win(self):
        board = TwixtBoard(SMALL_BOARD_SIZE)
        move = (3, 0)
        board.execute_move(move, RED)
        move = (1, 1)
        board.execute_move(move, BLACK)
        move = (4, 2)
        board.execute_move(move, RED)
        move = (3, 2)
        board.execute_move(move, BLACK)
        move = (3, 4)
        board.execute_move(move, RED)
        move = (2, 4)
        board.execute_move(move, BLACK)
        self.assertFalse(board.is_win(RED), "red should not win")
        self.assertFalse(board.is_win(BLACK), "black should not win")

        move = (1, 5)
        board.execute_move(move, RED)
        self.assertTrue(board.is_win(RED), "red should win ")


if __name__ == '__main__':
    unittest.main()
