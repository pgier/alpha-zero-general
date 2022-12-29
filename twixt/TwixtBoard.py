'''
Board class for the game of Twixt.

'''


class TwixtBoard():


    def __init__(self, n=3):
        self.n = n
        self.legalMoves = [0] * self.n * self.n
        return None

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.legalMoves[index]

    def get_legal_moves(self, color):
        moves = list()
        for i in range(len(self.legalMoves)):
            if self.legalMoves[i] == 0:
                new_move = (i % self.n, i//self.n)
                moves.append(new_move)
        print(moves)

        return moves

    def has_legal_moves(self):
        for i in range(len(self.legalMoves)):
            if self.legalMoves[i] == 0:
                return True
        return False
    
    def is_win(self, color):
        return None

    def execute_move(self, move, color):
        (x, y) = move
        pos = (y)*self.n + x
        assert self.legalMoves[pos] == 0
        self.legalMoves[pos] = color

