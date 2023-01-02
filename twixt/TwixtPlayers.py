import numpy as np

"""
Random and Human-interacting players for the game of Twixt.
"""


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
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i / self.game.size), int(i % self.game.size))
        while True:
            user_input = input()
            # Python 2.x
            # a = raw_input()

            x, y = [int(x) for x in user_input.split(' ')]
            a = self.game.size * x + y if x != -1 else self.game.size ** 2
            if valid[a]:
                break
            else:
                print('Invalid')

        return a
