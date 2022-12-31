"""
Board logic for the game of TwixT.
"""
import numpy
from logging import *

EMPTY = 0
RED = 1
BLACK = -1

color_name = {
    EMPTY: "empty",
    RED: "red",
    BLACK: "black",
}


class TwixtBoard:
    """
    Represents a Twixt board.  Red tries to cross the board top to bottom
    (y direction) while black tries to cross left to right (x direction).
    """
    GET_ALL = 2

    def __init__(self, size=24, handicap=0):
        """
        Initialize the board with the given side length (size).  An optional
        handicap can be provided which gives the red player an advantage by making
        the up/down (y diretion) size of the board shorter than the width (x direction).
        """
        self.n = size

        self.x = size
        self.y = size - handicap
        self.board = numpy.zeros((self.x, self.y), numpy.int8)

        # TODO: remove the `pegs` array and replace with the two dimensional `board` array
        self.pegs = [0] * self.n * self.n
        self.links_red = dict()
        self.links_black = dict()

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.board[index]

    def get(self, position):
        """ get the integer value (empty, red, black) at the given (x, y) position """
        (x, y) = position
        return self.board[x][y]

    def get_legal_moves(self, color):
        moves = list()
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j] == 0:
                    new_move = (i, j)
                    moves.append(new_move)
        print(moves)

        return moves
    def has_legal_moves(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.board[i][j] == 0:
                    return True
        return False

    def get_num(self, position):
        if type(position) is tuple:
            (x, y) = position
            pos = y * self.n + x
        else:
            pos = position
        return pos

    def get_tuple(self, position):
        if type(position) is int:
            pos = (position % self.n, position // self.n)
        else:
            pos = position
        return pos

    def get_links(self, position, color=GET_ALL):
        pos = self.get_num(position)
        if color == RED:
            return self.links_red[pos]
        elif color == BLACK:
            return self.links_black[pos]
        else:
            if pos in self.links_red:
                return self.links_red[pos]
            elif pos in self.links_black:
                return self.links_black[pos]
            else:
                return None

    def connect_link(self, position1, position2, color):
        if color == BLACK:
            if position1 not in self.links_black:
                self.links_black[position1] = set()

            if position2 not in self.links_black:
                self.links_black[position2] = set()

            self.links_black[position1].add(position2)
            self.links_black[position2].add(position1)
        if color == RED:
            if position1 not in self.links_red:
                self.links_red[position1] = set()

            if position2 not in self.links_red:
                self.links_red[position2] = set()
            self.links_red[position1]
            self.links_red[position1].add(position2)
            self.links_red[position2].add(position1)

    def check_links(self, position, color):
        pos = self.get_num(position)
        (x, y) = self.get_tuple(position)

        # Make sure it isn't along top row (0th row)
        if y > 0:
            # check (-2,-1)
            if x > 1 and self.pegs[pos - 2 - self.n] == color:
                log(DEBUG, "connection W by NW")
                self.connect_link(pos, pos - 2 - self.n, color)

            # check (+2,-1)
            if x < self.n - 2 and self.pegs[pos + 2 - self.n] == color:
                log(DEBUG, "connection E by NE")
                self.connect_link(pos, pos + 2 - self.n, color)

            # Make sure it isn't along top 2 rows (0th, 1st row)
            if y > 1:
                # check (-1,-2)
                if x > 0 and self.pegs[pos - 1 - self.n - self.n] == color:
                    log(DEBUG, "connection N by NW")
                    self.connect_link(pos, pos - 1 - self.n - self.n, color)

                # check (+1,-2)
                if x < self.n - 1 and self.pegs[pos + 1 - self.n - self.n] == color:
                    log(DEBUG, "connection N by NE")
                    self.connect_link(pos, pos + 1 - self.n - self.n, color)

        # Make sure it isn't along bottom row
        if y < self.n - 1:
            # check (+2,+1)
            if x < self.n - 2 and self.pegs[pos + 2 + self.n] == color:
                log(DEBUG, "connection E by SE")
                self.connect_link(pos, pos + 2 + self.n, color)

            # check (-2,+1)
            if x > 1 and self.pegs[pos - 2 + self.n] == color:
                log(DEBUG, "connection W by SW")
                self.connect_link(pos, pos - 2 + self.n, color)

            if y < self.n - 2:

                # check (+1,+2)
                if x < self.n - 1 and self.pegs[pos + 1 + self.n + self.n] == color:
                    log(DEBUG, "connection S by SE")
                    self.connect_link(pos, pos + 1 + self.n + self.n, color)

                # check (-1,+2)
                if x > 0 and self.pegs[pos - 1 + self.n + self.n] == color:
                    log(DEBUG, "connection S by SW")
                    self.connect_link(pos, pos - 1 + self.n + self.n, color)

        return len(self.links_red), len(self.links_black)



    def is_win(self, color):
        return False

    def execute_move(self, move, color):
        (x, y) = move
        assert self.board[x][y] == 0
        self.board[x][y] = color
        self.check_links(move, color)
