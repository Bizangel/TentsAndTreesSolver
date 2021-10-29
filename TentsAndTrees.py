from TentsAndTreesPuzzleInterface.imagedisplayer import DisplayPuzzle
from logica import Descriptor
import numpy as np
'''
TO REMEMBER:
GAME RULE IS TO PLACE TENTS IN THE BOARD.
1. EACH TREE HAS EXACTLY ONE TENT (ONE-TO-ONE)
2. EACH TENT MUST BE ADJACENT TO IT'S OWN TREE (BOTH HORIZONTALLY AND VERTICALLY, BUT NOT DIAGONALLY). However, a tent may be adjacent to other trees as well as its own.
3. NO TWO TENTS ARE ADJACENT. HORIZONTALLY, VERTICALLY NOR DIAGONALLY.
4. THE NUMBER OF TENTS IN EACH ROW, AND IN EACH COLUMN MUST MATCH THE NUMBERS GIVEN BY NEXT TO THE GRID.

# Some Implicit Basic rules
1. Tents can only be placed in empty spaces.
2. Clearly, our agent/player, can not change the position of trees nor the shape of the board.

TO NOTE:
We are marking empty assure spaces (squares where our agent, via rules and propositional logic has determined that such a square MUST be empty)
as GREEN or GREEN EMPTY squares.
These squares are not neccesary for the completion of the game and most variants of the game DO not include this feature.
However having a way to differentiate empty squares between assured empty green squares, makes it easier to implement our propositional logic for our agent.
'''


class TentsAndTrees:
    DisplayCodes = {
        0: "Empty",
        1: "Tree",
        2: "Tent",
        3: "Green",
    }

    def __init__(self, initial_matrix, row, col):
        ''' Creates a new puzzle, with given initial_matrix
        A square matrix of integers where each value represents a different square.
        0 -> empty (to be determined between green and tent)
        1 -> tree
        2 -> tent
        3 -> empty green (it is sure that it is empty)
        '''
        self.state = initial_matrix
        self.row = row
        self.col = col
        self.m, self.n = np.shape(initial_matrix)

    def displayState(self):
        return DisplayPuzzle(self.state, self.row, self.col)

    def transition(self, accion):
        ''' Performs the given action
        Action is a 3-tuple
        (x,y,val)
        Places respective value in respective x,y position.
        '''
        x, y, val = accion
        if (val == 1 or val == 0):
            raise ValueError("Can only place green squares or tents!. Trying to place {0}".format(
                TentsAndTrees.DisplayCodes[val]))

        if self.state[x, y] == 0:
            self.state[x, y] = val
        else:
            raise ValueError(
                "Can't play on square {0},{1}. Such a square is not empty (already filled with: {2})".format(x, y,
                                                                                                             TentsAndTrees.DisplayCodes[self.state[x, y]]))

    def checkDone(self):
        ''' Determines if the puzzle is done'''
        for row in self.m:
            pass # TODO

    def adjacentTiles(self, tile, includeDiagonals=False):
        ''' Returns adjacent tiles of given (x,y) tile'''
        adjacents = []
        x, y = tile
        # right
        if ((x + 1 < self.m)):
            adjacents.append((x+1, y))
        # left
        if ((x - 1 >= 0)):
            adjacents.append((x-1, y))
        # up
        if ((y + 1 < self.n)):
            adjacents.append((x, y + 1))
        # down
        if ((y - 1 >= 0)):
            adjacents.append((x, y - 1))

        if includeDiagonals:
            adjacents.extend(self.adjacentDiagonalTiles(x, y))
        return adjacents

    def adjacentDiagonalTiles(self, tile):
        ''' Returns adjacent diagonal tiles of given (x,y) tile'''
        diagonals = []
        x, y = tile
        # up right
        if ((x + 1 < self.m) and (y - 1 >= 0)):
            diagonals.append((x+1, y-1))
        # up left
        if ((x - 1 >= 0) and (y - 1 >= 0)):
            diagonals.append((x-1, y-1))
        # down right
        if ((x + 1 < self.m) and (y + 1 < self.n)):
            diagonals.append((x+1, y+1))
        # down left
        if ((x - 1 >= 0) and (y + 1 < self.n)):
            diagonals.append((x-1, y+1))

        return diagonals


# Our agent
# His main perception is sight. So he is able to determine the board and position of objects on the board,
# As well as row and col numbers (number of tents).


class Player:
    def __init__(self, puzzle, knowledge=None):
        self.puzzle = puzzle  # An instance of TentsAndTrees
        self.knowledge = None
        # Descriptor allows us to codificate propositions with a single letter/string
        # Propositions follow the pattern there is empty/tree/tent/green on position x,y
        self.cods = Descriptor([puzzle.m, puzzle.n, 4])

    def sense(self):
        ''' Returns our agents sight. The position of trees, greens and tents'''
        return self.puzzle.state  # Our agent can see the current state of the puzzle

    def make_sight_sentence(self):
        '''Creates propositional sentences out of perceived sight.'''
        sentences = []
        for i in range(self.m):
            for j in range(self.n):
                prop = self.cods([i, j, self.puzzle.state[i, j]])
                sentences.append(prop)
        return sentences
