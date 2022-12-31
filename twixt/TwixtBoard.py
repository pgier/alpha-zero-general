'''
Board class for the game of Twixt.

'''
import logging
from logging import *

BLACK = -1
RED = 1


class TwixtBoard:
    GET_ALL = 2

    def __init__(self, n=3):
        self.n = n
        self.pegs = [0] * self.n * self.n
        self.links_red = dict()
        self.links_black = dict()

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pegs[index]

    def get_legal_moves(self, color):
        moves = list()
        for i in range(len(self.pegs)):
            if self.pegs[i] == 0:
                new_move = (i % self.n, i // self.n)
                moves.append(new_move)
        print(moves)

        return moves

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

    def has_legal_moves(self):
        for i in range(len(self.pegs)):
            if self.pegs[i] == 0:
                return True
        return False

    def is_win(self, color):
        return False

    def execute_move(self, move, color):
        (x, y) = move
        pos = y * self.n + x
        assert self.pegs[pos] == 0
        self.pegs[pos] = color
        self.check_links(move, color)
