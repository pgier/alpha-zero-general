"""
Game implementation for the game of Twixt.
"""

import numpy as np
from Game import Game
from twixt.TwixtBoard import TwixtBoard


class TwixtGame(Game):
    """
    TwixtGame manages the current state of the game.
    """

    def __init__(self, size=24, handicap=0):
        self.size = size
        self.handicap = handicap
        self.x = self.size
        self.y = self.size - handicap

    def getInitBoard(self):
        b = TwixtBoard(self.size, self.handicap)
        return b.board

    def getBoardSize(self):
        return self.x, self.y

    def getActionSize(self):
        # TODO: why do we need to add 1, is this for resignation?
        return self.x * self.y + 1

    def getNextState(self, board, player, action):
        # TODO: why can't we just store a TwixtBoard in the object state instead of re-creating it every turn?
        b = TwixtBoard(self.size, self.handicap)
        b.board = np.copy(board)
        move = (action % self.x, action // self.y)
        b.execute_move(move, player)
        return b.board, -player

    def getValidMoves(self, board, player):
        valid_moves = [0] * self.getActionSize()
        b = TwixtBoard(self.size, self.handicap)
        b.board = np.copy(board)
        legal_moves = b.get_legal_moves(player)
        if len(legal_moves) == 0:
            valid_moves[-1] = 1
            return np.array(valid_moves)
        for x, y in legal_moves:
            valid_moves[self.size * y + x] = 1
        return np.array(valid_moves)

    def getGameEnded(self, board, player):
        b = TwixtBoard(self.size, self.handicap)
        b.board = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value
        return 1e-4

    def getCanonicalForm(self, board, player):
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.y, self.x))
        board_list = []

        for i in range(1, 5):
            for j in [True, False]:
                new_board = np.rot90(board, i)
                new_pi = np.rot90(pi_board, i)
                if j:
                    new_board = np.fliplr(new_board)
                    new_pi = np.fliplr(new_pi)
                board_list += [(new_board, list(new_pi.ravel()) + [pi[-1]])]
        return board_list

    def stringRepresentation(self, board):
        return board.tostring()

    @staticmethod
    def display(board):
        print("-TwixT-")
        bx, by = board.shape
        # by = board.y
        vx = 0
        vy = by - 1
        nx = 0
        ny = by - 1
        for y in reversed(range(by)):
            print(ny, end="  ")
            for x in range(bx):
                value = board[x][y]
                if value == 1:
                    print("r", end="  ")
                elif value == -1:
                    print("b", end="  ")
                else:
                    print("e", end="  ")
            print()
            vy -= 1
            ny -= 1
        print("x", end="  ")
        for n in range(bx):
            print(vx, end="  ")
            vx += 1
        print()
