"""
Game implementation for the game of Twixt.
"""

from Game import Game


class TwixtGame(Game):
    """
    TwixtGame class manages the current state of the game.
    """

    def __init__(self, n=6):
        self.n = n

    def getInitBoard(self):
        return None

    def getBoardSize(self):
        return None

    def getActionSize(self):
        return None

    def getNextState(self, board, player, action):
        return None

    def getValidMoves(self, board, player):
        return None

    def getGameEnded(self, board, player):
        return None

    def getCanonicalForm(self, board, player):
        return None

    def getSymmetries(self, board, pi):
        return None

    def stringRepresentation(self, board):
        return None

    @staticmethod
    def display(board):
        print("nothing here")
