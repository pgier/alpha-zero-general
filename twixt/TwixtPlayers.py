"""
Random and Human-interacting players for the game of Twixt.
"""
import numpy as np
import sys


class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valid_moves = self.game.getValidMoves(board, 1)
        while valid_moves[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
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
                print("Invalid move, this position is already taken")

    @staticmethod
    def done():
        print("Bye")
        sys.exit()
