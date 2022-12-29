"""
Unit Tests for the TwixtGame class
"""
import unittest

from twixt.TwixtGame import TwixtGame

TEST_BOARD_SIZE = 12

class TestTwixtBoard(unittest.TestCase):

    def setUp(self):
        self.game = TwixtGame(TEST_BOARD_SIZE)

    def testGetBoardSize(self):
        currentBoardSize = self.game.getBoardSize()
        self.assertEqual(TEST_BOARD_SIZE, currentBoardSize)

    def testGetInitBoard(self):
        initialBoard = self.game.getInitBoard()
        self.assertIsNotNone(initialBoard)

if __name__ == '__main__':
    unittest.main()
