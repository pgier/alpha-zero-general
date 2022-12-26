import os

# os.environ['CUDA_VISIBLE_DEVICES'] = "0"

import Arena
from MCTS import MCTS
from tictactoe.TicTacToeGame import TicTacToeGame
from tictactoe.TicTacToePlayers import *
from tictactoe.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""


def main():
    g = TicTacToeGame()
    random_player = RandomPlayer(g).play
    human_player = HumanTicTacToePlayer(g).play

    n1 = NNet(g)
    n1.load_checkpoint('./temp/ttt_checkpoint', 'temp.h5')

    args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)

    def nn_player(x): return np.argmax(mcts1.getActionProb(x, temp=0))
    # nn_player = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

    arena = Arena.Arena(nn_player, human_player, g, display=TicTacToeGame.display)

    print(arena.playGames(2, verbose=True))


if __name__ == "__main__":
    main()
