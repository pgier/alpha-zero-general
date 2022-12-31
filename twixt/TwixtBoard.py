'''
Board class for the game of Twixt.

'''


class TwixtBoard():
    BLACK = -1
    RED = 1

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

    def connect_link(self, position1, position2, color):
        connected = (position1, position2)
        if color == self.BLACK:
            if self.linksBLACK[position1] is None:
                self.linksBLACK[position1] = set()

            if self.linksBLACK[position2] is None:
                self.linksBLACK[position2] = set()

            self.linksBLACK[position1].add(position2)
            self.linksBLACK[position2].add(position1)
        if color == self.RED:
            if self.linksRED[position1] is None:
                self.linksRED[position1] = set()

            if self.linksRED[position2] is None:
                self.linksRED[position2] = set()

            self.linksRED[position1].add(position2)
            self.linksRED[position2].add(position1)

    def check_links(self, position, color):
        if type(position) is tuple:
            (x, y) = position
            pos = y * self.n + x
        else:
            pos = position

        # Make sure it isn't along top row (0th row)
        if pos >= self.n:
            # check (-2,-1)
            if self.pegs[pos - 2 - self.n] == color and pos % self.n > 1:
                print("connection W by NW")
                self.connect_link(pos, pos - 2 - self.n, color)

            # check (+2,-1)
            if self.pegs[pos + 2 - self.n] == color and pos % self.n < self.n - 2:
                print("connection E by NE")
                self.connect_link(pos, pos + 2 - self.n, color)

            # Make sure it isn't along top 2 rows (0th, 1st row)
            if pos > (self.n * 2):
                # check (-1,-2)
                if self.pegs[pos - 1 - self.n - self.n] == color and pos % self.n != 0:
                    print("connection N by NW")
                    self.connect_link(pos, pos - 1 - self.n - self.n, color)

                # check (+1,-2)
                if self.pegs[pos + 1 - self.n - self.n] == color and pos % self.n != self.n - 1:
                    print("connection N by NE")
                    self.connect_link(pos, pos + 1 - self.n - self.n, color)

        # Make sure it isn't along bottom row
        if pos < (self.n * self.n - self.n):
            # check (+2,+1)
            if self.pegs[pos + 2 + self.n] == color and pos % self.n < self.n - 2:
                print("connection E by SE")
                self.connect_link(pos, pos + 2 + self.n, color)

            # check (-2,+1)
            if self.pegs[pos - 2 + self.n] == color and pos % self.n > 1:
                print("connection W by SW")
                self.connect_link(pos, pos - 2 + self.n, color)

            if pos < (self.n * self.n - self.n - self.n):

                # check (+1,+2)
                if self.pegs[pos + 1 + self.n + self.n] == color and pos % self.n != self.n - 1:
                    print("connection S by SE")
                    self.connect_link(pos, pos + 1 + self.n + self.n, color)

                # check (-1,+2)
                if self.pegs[pos - 1 + self.n + self.n] == color and pos % self.n != 0:
                    print("connection S by SW")
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
