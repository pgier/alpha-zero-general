"""
Random and Human-interacting players for the game of Twixt.
"""
import numpy as np
import sys

from twixt.TwixtBoard import RED

class RandomPlayer:
    def __init__(self, game, color=RED):
        self.game = game
        self.color = color

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valid_moves = self.game.getValidMoves(board, self.color)
        while valid_moves[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        (board_x, _) = board.shape
        (x, y) = (a % board_x, a // board_x)
        print("random move: {0} {1}".format(x, y))
        return a


class HumanPlayer:
    def __init__(self, game, color=RED):
        self.game = game
        self.color = color

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, self.color)
        (board_x, board_y) = board.shape
        # for i in range(len(valid)):
        #     if valid[i]:
        #         print(int(i / self.game.size), int(i % self.game.size))
        while True:
            try:
                raw_in = input()
            except EOFError:
                HumanPlayer.done()

            trimmed_input = raw_in.strip()
            if trimmed_input == "q" or trimmed_input == "quit":
                HumanPlayer.done()

            split_input = trimmed_input.split(' ')
            if len(split_input) != 2:
                print("Invalid input, enter position `x y` or `q` to quit")
                continue
            x, y = [int(x) for x in split_input]
            selected_move = board_x * y + x if x != -1 else board_x * board_y
            if valid_moves[selected_move]:
                return selected_move
            else:
                print("Invalid move, please try again")

    @staticmethod
    def done():
        print("Bye")
        sys.exit()
