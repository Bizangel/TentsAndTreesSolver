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

PUZZLES ARE DETERMINISTIC. THERE ARE NO TWO SOLUTIONS TO A PUZZLE.
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
        self.row = [int(x) for x in row]
        self.col = [int(x) for x in col]
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
        # Check That there's number of tents equal to the side.

        for row in range(self.m):
            if (np.sum(self.state[row, :] == 2) != int(self.row[row])):
                return False

        totaltents = 0
        for col in range(self.n):
            tentsoncol = np.sum(self.state[:, col] == 2)
            totaltents += tentsoncol
            if (tentsoncol != int(self.col[col])):
                return False

        # count total trees, must be one to one with trees
        totaltrees = sum([np.sum(self.state[:, col] == 1)
                          for col in range(self.n)])
        if (totaltents != totaltrees):
            return False

        # Check that every tent is adjacent to a tree.
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i, j] == 2:
                    # check that there's a tree to each adjacent tent.
                    if 1 not in [self.state[x, y] for x, y in self.adjacentTiles((i, j))]:
                        return False
        # Check that every tree has at least a tent!
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i, j] == 1:
                    # check that there's a tent to each tree
                    if 2 not in [self.state[x, y] for x, y in self.adjacentTiles((i, j))]:
                        return False

        # Check that no two tents are adjacent (even diagonally).
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i, j] == 2:
                    if 2 in [self.state[x, y] for x, y in self.adjacentTiles((i, j), True)]:
                        return False

        return True  # passed all checks

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
            adjacents.extend(self.adjacentDiagonalTiles((x, y)))
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

        # Will codify row and column numbers of tents (adjacent to board).
        # First entry means either row or col.
        # 0-> row
        # 1-> col
        # Second entry means row/col number (index)
        # Third entry represents actual number in row.
        # Ex: numberCods.P([1,3,2]) means there must be 2 tents, on column of index 3.
        # Ex: numberCods.P([0,1,4]) means there must be 4 tents, on row of index 1.
        self.numberCods = Descriptor(
            [2, max(self.puzzle.m, self.puzzle.n), max(max(puzzle.row), max(puzzle.col)) + 1], chrInit=(256+self.puzzle.m*self.puzzle.n*4+100))
        # make sure that chrInit is enough far away, so there is no collision with self.cods

    def make_sight_sentence(self):
        '''Creates propositional sentence out of perceived sight.'''
        # agent can see the board.
        sentences = ""
        for i in range(self.puzzle.m):
            for j in range(self.puzzle.n):
                prop = self.cods.P([i, j, self.puzzle.state[i, j]])
                # sentences.append(prop)
                sentences += "Y" + prop
        # agent can see the adjacent board numbers.
        # add row numbers
        for i in range(self.puzzle.m):
            sentences += "Y" + self.numberCods.P([0, i, self.puzzle.row[i]])
        # add col numbers
        for i in range(self.puzzle.n):
            sentences += "Y" + self.numberCods.P([1, i, self.puzzle.col[i]])
        return sentences

    def acknowledge_sight(self):
        ''' Adds the sight propositional sentences to the Agent's knowledge database'''
        self.knowledge.TELL(self.make_sight_sentence())

    def make_emptygreen_rule(self):
        ''' If Adjacent Tiles are not TREES AND Square is not a tree. Then square must be green'''
        rules = []
        for i in range(self.puzzle.m):
            for j in range(self.puzzle.n):
                adja_negation = 'Y'.join(
                    ['-' + self.cods.P([x, y, 1]) for x, y in self.puzzle.adjacentTiles((i, j))])
                rules.append(adja_negation + 'Y-' + self.cods.P([i, j, 1]) + '>' +
                             self.cods.P([i, j, 3]))
        return rules

    def make_unique_rule(self):
        ''' We implicitly know that if a square is set, then all other possibilities must be discarded. If a tree is on (x,y) then clearly there cannot be a tent on (x,y)'''
        rules = []
        for i in range(self.puzzle.m):
            for j in range(self.puzzle.n):
                # if there's a tree/tent/green on a square, then there must not be anything else on that square.
                for val in range(1, 4):  # exclude empty squares from rule
                    for otherval in [otherval for otherval in range(4) if otherval != val]:
                        rules.append(self.cods.P(
                            [i, j, val]) + ">-" + self.cods.P([i, j, otherval]))
                # if a square it's empty, then it can be replaced. So we cannot simply ignore all other possibilities, or else we fall in a contradiction
                # However, if a square it's empty, we know that a tree CANNOT be there.
                rules.append(self.cods.P([i, j, 0]) +
                             '>-' + self.cods.P([i, j, 1]))
        return rules

    def make_emptyrowcol_rule(self):
        '''If there is a zero, on corresponding square or row, then there must be no tents on said square (square must be green)'''
        rules = []
        for i in range(self.puzzle.m):
            for j in range(self.puzzle.n):
                # if square is not a tree
                # and square square's row number is 0
                # then square must be green
                rules.append('-' + self.cods.P([i, j, 1]) + 'Y' +
                             self.numberCods.P([0, i, 0]) + '>' + self.cods.P([i, j, 3]))
                # same but with column
                rules.append('-' + self.cods.P([i, j, 1]) + 'Y' +
                             self.numberCods.P([1, j, 0]) + '>' + self.cods.P([i, j, 3]))
        return rules

    def place_adjacent_tent_rule(self):
        '''If there is only an empty adjacent square to a tree, then there must be a tent in that square'''
        rules = []
        for i in range(self.puzzle.m):
            for j in range(self.puzzle.n):

                body = self.cods.P([i, j, 1])
                adjacents = self.puzzle.adjacentTiles(
                    (i, j), includeDiagonals=False)

                for x1, y1 in adjacents:
                    othersquares_neg = 'Y'.join([
                        '-' + self.cods.P([x2, y2, 1]) + 'Y-' + self.cods.P([x2, y2, 2]) for x2, y2 in adjacents if (x1, y1) != (x2, y2)])
                    squarebody = self.cods.P([x1, y1, 0])
                    rules.append(body + 'Y' + squarebody +
                                 'Y' + othersquares_neg + '>' + self.cods.P([x1, y1, 2]))

        return rules

    def humanReadAtom(self, atom):
        neg = False
        if atom[0] == '-':
            neg = True
            atom = atom[1]

        x, y, code = self.cods.inv(atom)
        code = TentsAndTrees.DisplayCodes[code]
        if neg:
            return f'NOT {code} on ({x},{y})'
        else:
            return f'{code} on ({x},{y})'

    def humanReadFormula(self, proposition):
        [prev, conclusion] = proposition.split('>')

        prevs = prev.split('Y')

        nots = [x[0] == '-' for x in prevs]

        characters = []
        for x in prevs:
            if (x[0] == '-'):
                characters.append(x[1])
            else:
                characters.append(x[0])

        xs = [self.cods.inv(x)[0] for x in characters]
        ys = [self.cods.inv(x)[1] for x in characters]
        codes = [TentsAndTrees.DisplayCodes[self.cods.inv(
            x)[2]] for x in characters]

        conclusionNegated = False
        if conclusion[0] == '-':
            conclusionNegated = True
            conclusion = conclusion[0]

        xc, yc, code_c = self.cods.inv(conclusion)
        code_c = TentsAndTrees.DisplayCodes[code_c]

        buildstr = "IF: "
        n = len(xs)
        for i in range(n):
            x, y, code = xs[i], ys[i], codes[i]
            if (nots[i]):
                buildstr += f"NOT {code} in ({x},{y})"
            else:
                buildstr += f"{code} in ({x},{y})"
            if (i != n-1):
                buildstr += " AND "

        concstring = f"{xc},{yc},{code_c}"
        if conclusionNegated:
            concstring = "NOT" + concstring

        return buildstr + " IMPLIES " + f"{code_c} ON ({xc},{yc})"
