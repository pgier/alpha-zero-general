'''
Board class for the game of Twixt.

'''
import logging
from logging import *
class TwixtBoard():
    BLACK = -1
    RED = 1
    GETALL = 2
    def __init__(self, n=3):
        self.n = n
        self.pegs = [0] * self.n * self.n
        self.linksRED = dict()
        self.linksBLACK = {}
        return None

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

    def get_links(self, position, color=GETALL):
        pos = self.get_num(position)
        if color == self.RED:
            return self.linksRED[pos]
        elif color == self.BLACK:
            return self.linksBLACK[pos]
        else:
            if pos in self.linksRED:
                return self.linksRED[pos]
            elif pos in self.linksBLACK:
                return self.linksBLACK[pos]
            else:
                return None

    def connect_link(self, position1, position2, color):
        if color == self.BLACK:
            if position1 not in self.linksBLACK:
                self.linksBLACK[position1] = set()

            if position2 not in self.linksBLACK:
                self.linksBLACK[position2] = set()

            self.linksBLACK[position1].add(position2)
            self.linksBLACK[position2].add(position1)
        if color == self.RED:
            if position1 not in self.linksRED:
                self.linksRED[position1] = set()

            if position2 not in self.linksRED:
                self.linksRED[position2] = set()
            self.linksRED[position1]
            self.linksRED[position1].add(position2)
            self.linksRED[position2].add(position1)

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

        return len(self.linksRED), len(self.linksBLACK)

    def has_legal_moves(self):
        for i in range(len(self.pegs)):
            if self.pegs[i] == 0:
                return True
        return False

    def is_win(self, color):
        return None

    def execute_move(self, move, color):
        (x, y) = move
        pos = y * self.n + x
        assert self.pegs[pos] == 0
        self.pegs[pos] = color
        self.check_links(move, color)
