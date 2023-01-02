
import logging

from Coach import Coach
from twixt.TwixtGame import TwixtGame
from twixt.keras.NNet import NNetWrapper
from utils import *

log = logging.getLogger(__name__)

args = dotdict({
    'numIters': 1,
    'numEps': 10,               # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 3,

    'checkpoint': './temp/ttt_checkpoint',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.ttt.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def main():
    print("Starting TicTacToe...")
    g = TicTacToeGame()

    log.info('Loading %s...', NNetWrapper.__name__)
    nnet = NNetWrapper(g)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
