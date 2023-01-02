"""
Board logic for the game of TwixT.
"""
import numpy as np
from logging import *
from twixt.TwixtUtil import *

EMPTY = 0
RED = 1
BLACK = -1

color_name = {
    EMPTY: "empty",
    RED: "red",
    BLACK: "black",
}

GET_ALL = 2

# Link direction masks.  These are used to
# store all possible links in a single int16.
# Each direction corresponds to a single bit.
NORTH_NE = 2  # x + 1, y + 2
EAST_NE = 4
EAST_SE = 8
SOUTH_SE = 16
SOUTH_SW = 32
WEST_SW = 64
WEST_NW = 128
NORTH_NW = 256

# OFFSETs are used to calculate the position of a connected
# peg based on the link direction.
NORTH_NE_OFFSET = (1, 2)
EAST_NE_OFFSET = (2, 1)
EAST_SE_OFFSET = (2, -1)
SOUTH_SE_OFFSET = (1, -2)
SOUTH_SW_OFFSET = (-1, -2)
WEST_SW_OFFSET = (-2, -1)
WEST_NW_OFFSET = (-2, 1)
NORTH_NW_OFFSET = (-1, 2)

LINK_OFFSET_DICT = {
    EMPTY: (0, 0),
    NORTH_NE: NORTH_NE_OFFSET,
    EAST_NE: EAST_NE_OFFSET,
    EAST_SE: EAST_SE_OFFSET,
    SOUTH_SE: SOUTH_SE_OFFSET,
    SOUTH_SW: SOUTH_SW_OFFSET,
    WEST_SW: WEST_SW_OFFSET,
    WEST_NW: WEST_NW_OFFSET,
    NORTH_NW: NORTH_NW_OFFSET,
}

LINK_REVERSE_DICT = {
    EMPTY: EMPTY,
    NORTH_NE: SOUTH_SW,
    EAST_NE: WEST_SW,
    EAST_SE: WEST_NW,
    SOUTH_SE: NORTH_NW,
    SOUTH_SW: NORTH_NE,
    WEST_SW: EAST_NE_OFFSET,
    WEST_NW: EAST_SE_OFFSET,
    NORTH_NW: SOUTH_SE_OFFSET,
}


class TwixtBoard:
    """
    Represents a Twixt board.  Red tries to cross the board top to bottom  (y direction) while black
    tries to cross left to right (x direction). An optional handicap can be provided which gives the
    red player an advantage by making the up/down (y direction) size of the board shorter than the
    width (x direction).
    """

    def __init__(self, size=24, handicap=0, state=None):
        """
        Initialize the board with the given side length (size) and handicap, or initialize the board based
        on the given board state which must be a numpy.ndarray.
        """
        if state is None:
            self.x = size
            self.y = size - handicap
            self.state = np.zeros((self.x, self.y), np.int16)
        elif isinstance(state, np.ndarray):
            (self.x, self.y) = state.shape
            self.handicap = self.x - self.y
        else:
            raise Exception(
                "Invalid type for board state.  Expected `None` or `numpy.ndarray`, got {0}".format(type(state)))

        # TODO: remove the `links` dictionaries and store the links in the two dimensional `board` array
        self.links_red = dict()
        self.links_black = dict()

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.state[index]

    def get(self, x=0, y=0, offset=(0, 0)):
        """ Get the board state at the given (x, y) position with an optional offset"""
        (a, b) = offset
        return self.state[x + a][y + b]

    def get_legal_moves(self, color):
        moves = list()
        for i in range(self.x):
            for j in range(self.y):
                if self.state[i][j] == 0:
                    new_move = (i, j)
                    moves.append(new_move)
        return moves

    def has_legal_moves(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.state[i][j] == 0:
                    return True
        return False

    def get_num(self, position):
        if type(position) is tuple:
            (x, y) = position
            pos = y * self.x + x
        else:
            pos = position
        return pos

    def get_tuple(self, position):
        if type(position) is int:
            pos = (position % self.x, position // self.x)
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

    def connect_link(self, x, y, direction, color):
        """ Link the given x, y peg to the peg in the given direction (if not blocked) """
        p1 = (x, y)
        (ox, oy) = LINK_OFFSET_DICT[direction]
        (x2, y2) = (x + ox, y + oy)
        p2 = (x2, y2)

        if self.check_blocks(p1, p2):
            self.state[x][y] = set_bits(self.state[x][y], direction)
            self.state[x2][y2] = set_bits(self.state[x2][y2], LINK_REVERSE_DICT(direction))

        # TODO: this section maybe can be removed
        if color == BLACK:
            if p1 not in self.links_black:
                self.links_black[p1] = set()

            if p2 not in self.links_black:
                self.links_black[p2] = set()

            if self.check_blocks(p1, p2):
                self.links_black[p1].add(p2)
                self.links_black[p2].add(p1)
        if color == RED:
            if p1 not in self.links_red:
                self.links_red[p1] = set()

            if p2 not in self.links_red:
                self.links_red[p2] = set()

            if self.check_blocks(p1, p2):
                self.links_red[p1].add(p2)
                self.links_red[p2].add(p1)
        # TODO: end remove section

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
                    if self.state[xi + x1][yi + y1] != 0:
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

    def update_links(self, position, color):
        """
        Find and create links which are made possible by the new peg at `position`.
        Position must be an (x, y) tuple.
        """

        (x, y) = position

        # Make sure it isn't along the bottom row (0th row)
        if y > 0:
            # check (-2,-1)
            if x > 1 and (color * self.get(x, y, WEST_NW_OFFSET)) > 0:
                log(DEBUG, "connection W by NW")
                self.connect_link(position, (x - 2, y - 1), color)

            # check (+2,-1)
            if x < self.x - 2 and (color * self.get(x, y, EAST_NE_OFFSET)) > 0:
                log(DEBUG, "connection E by NE")
                self.connect_link(position, (x + 2, y - 1), color)

            # Make sure it isn't along top 2 rows (0th, 1st row)
            if y > 1:
                # check (-1,-2)
                if x > 0 and self.state[x - 1][y - 2] == color:
                    log(DEBUG, "connection N by NW")
                    self.connect_link(position, (x - 1, y - 2), color)

                # check (+1,-2)
                if x < self.x - 1 and self.state[x + 1][y - 2] == color:
                    log(DEBUG, "connection N by NE")
                    self.connect_link(position, (x + 1, y - 2), color)

        # Make sure it isn't along top row
        if y < self.y - 1:
            # check (+2,+1)
            if x < self.x - 2 and self.state[x + 2][y + 1] == color:
                log(DEBUG, "connection E by SE")
                self.connect_link(position, (x + 2, y + 1), color)

            # check (-2,+1)
            if x > 1 and self.state[x - 2][y + 1] == color:
                log(DEBUG, "connection W by SW")
                self.connect_link(position, (x - 2, y + 1), color)

            if y < self.y - 2:

                # check (+1,+2)
                if x < self.x - 1 and self.state[x + 1][y + 2] == color:
                    log(DEBUG, "connection S by SE")
                    self.connect_link(position, (x + 1, y + 2), color)

                # check (-1,+2)
                if x > 0 and self.state[x - 1][y + 2] == color:
                    log(DEBUG, "connection S by SW")
                    self.connect_link(position, (x - 1, y + 2), color)

        return len(self.links_red), len(self.links_black)

    def is_win(self, color):
        # TODO: needs to be implemented, remove temporary testing logic
        if self.state[0][0] != 0:
            return True
        return False

    def execute_move(self, move, color):
        (x, y) = move
        assert self.state[x][y] == 0
        self.state[x][y] = color
        self.update_links(move, color)
