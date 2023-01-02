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
        pos = self.get_tuple(position)
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

            if self.check_blocks(position1, position2):
                self.links_black[position1].add(position2)
                self.links_black[position2].add(position1)
        if color == RED:
            if position1 not in self.links_red:
                self.links_red[position1] = set()

            if position2 not in self.links_red:
                self.links_red[position2] = set()

            if self.check_blocks(position1, position2):
                self.links_red[position1].add(position2)
                self.links_red[position2].add(position1)

    def check_blocks(self, pos1, pos2):
        '''pos1 and pos2 are tuples'''
        # 4 different types: check 3x2 area for links
        (x1, y1) = pos1
        (x2, y2) = pos2
        (xdiff, ydiff) = (x2 - x1, y2 - y1)
        (vert, horiz) = (xdiff % 2, ydiff % 2)  # vert is 1 when vertical, horiz is 1 when horizontal
        if xdiff * ydiff > 0:
            slope = True
        else:
            slope = False
        blocked = False
        a_block = list()
        b_block = list()
        a_block.append((vert - horiz + max(x1, x2),
                        vert - horiz + min(y1, y2)))
        a_block.append((-vert + horiz + min(x1, x2),
                        -vert + horiz + max(y1, y2)))
        b_block.append((-vert + min(x1, x2),
                        horiz + max(y1, y2)))
        b_block.append((-vert + min(x1, x2),
                        -horiz + min(y1, y2)))
        b_block.append((vert + max(x1, x2),
                        min(y1, y2) - horiz))
        b_block.append((vert + max(x1, x2),
                        horiz + max(y1, y2)))
        if slope:
            b_block.append((horiz + max(x1, x2),
                            min(y1, y2) - vert))
            b_block.append((min(x1, x2) - horiz,
                            max(y1, y2 + vert)))
        else:
            b_block.append((min(x1, x2) - horiz,
                            min(y1, y2) - vert))
            b_block.append((max(x1, x2) + horiz,
                            max(y1, y2) + vert))
        xi = 0
        while - 3 + vert < xi < 3 - vert:
            yi = 0
            while - 3 + horiz < yi < 3 - horiz:
                if (xi != 0 or yi != 0) and (xi + x1 != x2 or yi + y1 != y2):
                    if self.board[xi + x1][yi + y1] != 0:
                        if self.get_links(((xi + x1), (y1 + yi))):
                            if (vert * yi + horiz * xi == 0) or (
                                    vert * (yi + y1) + horiz * (xi + x1) == vert * y2 + horiz * x2):
                                for i in range(len(a_block)):

                                    if a_block[i] in self.get_links(((xi + x1), (yi + y1))):
                                        return blocked
                                a_block.append(((xi + x1), (yi + y1)))
                            else:
                                for i in range(len(b_block)):
                                    if b_block[i] in self.get_links(((xi + x1), (yi + y1))):
                                        return blocked
                yi = (yi + vert * ydiff // 2 + horiz * ydiff)
            xi = (xi + horiz * xdiff // 2 + vert * xdiff)
        return not blocked

    def check_links(self, position, color):
        """ position is ALWAYS tuple """

        (x, y) = position

        # Make sure it isn't along top row (0th row)
        if y > 0:
            # check (-2,-1)
            if x > 1 and self.board[x - 2][y - 1] == color:
                log(DEBUG, "connection W by NW")
                self.connect_link(position, (x - 2, y - 1), color)

            # check (+2,-1)
            if x < self.x - 2 and self.board[x + 2][y - 1] == color:
                log(DEBUG, "connection E by NE")
                self.connect_link(position, (x + 2, y - 1), color)

            # Make sure it isn't along top 2 rows (0th, 1st row)
            if y > 1:
                # check (-1,-2)
                if x > 0 and self.board[x - 1][y - 2] == color:
                    log(DEBUG, "connection N by NW")
                    self.connect_link(position, (x - 1, y - 2), color)

                # check (+1,-2)
                if x < self.x - 1 and self.board[x + 1][y - 2] == color:
                    log(DEBUG, "connection N by NE")
                    self.connect_link(position, (x + 1, y - 2), color)

        # Make sure it isn't along bottom row
        if y < self.y - 1:
            # check (+2,+1)
            if x < self.x - 2 and self.board[x + 2][y + 1] == color:
                log(DEBUG, "connection E by SE")
                self.connect_link(position, (x + 2, y + 1), color)

            # check (-2,+1)
            if x > 1 and self.board[x - 2][y + 1] == color:
                log(DEBUG, "connection W by SW")
                self.connect_link(position, (x - 2, y + 1), color)

            if y < self.y - 2:

                # check (+1,+2)
                if x < self.x - 1 and self.board[x + 1][y + 2] == color:
                    log(DEBUG, "connection S by SE")
                    self.connect_link(position, (x + 1, y + 2), color)

                # check (-1,+2)
                if x > 0 and self.board[x - 1][y + 2] == color:
                    log(DEBUG, "connection S by SW")
                    self.connect_link(position, (x - 1, y + 2), color)

        return len(self.links_red), len(self.links_black)

    def is_win(self, color):
        return False

    def execute_move(self, move, color):
        (x, y) = move
        assert self.board[x][y] == 0
        self.board[x][y] = color
        self.check_links(move, color)
