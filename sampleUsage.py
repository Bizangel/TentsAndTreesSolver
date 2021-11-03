''' Sample '''
import collections
from TentsAndTreesPuzzleInterface.PuzzleStorage import StorePuzzle, LoadStoredPuzzle
from TentsAndTrees import TentsAndTrees, Player
import numpy as np
from TentsAndTreesPuzzleInterface.imagereader import FetchAndParsePuzzle
from logica import LPQuery, ASK, pl_fc_ask

# matrix, row, col = FetchAndParsePuzzle("Puzzles/puzzle5.png")
# StorePuzzle("Puzzles/puzzle5.npz", matrix, row, col)

matrix, row, col = LoadStoredPuzzle("Puzzles/puzzle1.npz")
puzzle = TentsAndTrees(matrix, row, col)


myplayer = Player(puzzle)

myplayer.knowledge = LPQuery(
    myplayer.make_emptygreen_rule() +
    myplayer.make_unique_rule() +
    myplayer.make_emptyrowcol_rule() +
    myplayer.place_adjacent_tent_rule() +
    myplayer.make_emptygreen_adjacent_to_tent_rule() +
    myplayer.fillRemainingEqual() +
    myplayer.fillRemainingEqualEmpty()
)

namerules = [rule.nombre for rule in myplayer.knowledge.reglas]

assert len(namerules) == len(set(namerules)), "There are duplicate rules!"


''' Atom initialization for Forward Chaining '''
atoms = []
for i in range(2):
    for j in range(max(puzzle.m, puzzle.n)):
        for v in range(max(max(puzzle.row), max(puzzle.col)) + 1):
            atoms.append(myplayer.numberCods.P([i, j, v]))
            atoms.append('-' + myplayer.numberCods.P([i, j, v]))

for i in range(puzzle.m):
    for j in range(puzzle.n):
        for v in range(4):
            atoms.append(myplayer.cods.P([i, j, v]))
            atoms.append('-' + myplayer.cods.P([i, j, v]))

myplayer.knowledge.atomos = atoms


def findFirstGreen():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                # play and reset
                print(f"Asking Green --- {i} {j} ")
                if ASK(myplayer.cods.P([i, j, 3]), 'success', myplayer.knowledge):
                    print(f"{i} {j} IS Green!")
                    puzzle.transition([i, j, 3])
                    found = True
                    break
        if found:
            break
    return found


def findFirstGreenFC():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                # play and reset
                print(f"Asking Green --- {i} {j} ")
                if pl_fc_ask(myplayer.cods.P([i, j, 3]), myplayer.knowledge):
                    print(f"{i} {j} IS Green!")
                    puzzle.transition([i, j, 3])
                    found = True
                    break
        if found:
            break
    return found


def findFirstTent():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                print(f"Asking Tent --- {i} {j} ")
                if ASK(myplayer.cods.P([i, j, 2]), 'success', myplayer.knowledge):
                    print(f"{i} {j} IS Tent!")
                    puzzle.transition([i, j, 2])
                    found = True
                    break
        if found:
            break
    return found


def findFirstTentFC():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                print(f"Asking Tent --- {i} {j} ")
                if pl_fc_ask(myplayer.cods.P([i, j, 2]), myplayer.knowledge):
                    print(f"{i} {j} IS Tent!")
                    puzzle.transition([i, j, 2])
                    found = True
                    break
        if found:
            break
    return found


def easyAsk(charatom):

    if ASK(charatom, 'success', myplayer.knowledge):
        return True
    elif ASK('-' + charatom, 'success', myplayer.knowledge):
        return False
    else:
        return "Unknown"


def fullyAskTile(i, j):
    print(f"------- TILE ({i},{j}) ---------")
    for value in range(1, 4):
        queryval = ASK(
            myplayer.cods.P([i, j, value]), 'success', myplayer.knowledge)
        msg = "True" if queryval else "Unknown"
        print(
            f"Is there {TentsAndTrees.DisplayCodes[value]} in ({i},{j})?: {msg} ")

    # negations
    for value in range(1, 4):
        queryval = ASK(
            '-' + myplayer.cods.P([i, j, value]), 'success', myplayer.knowledge)
        msg = "True" if queryval else "Unknown"
        print(
            f"Is there NOT {TentsAndTrees.DisplayCodes[value]} in ({i},{j})?: {msg} ")


def displayknowledge():
    print("The agent knows: ----------------")
    for dat in myplayer.knowledge.datos:
        print(myplayer.humanReadAtom(dat))
    print('-------------------------')


while True:
    myplayer.acknowledge_sight()
    # displayknowledge()
    if findFirstGreenFC():
        # print("Found Green")
        continue

    if findFirstTentFC():
        # print("Found Tent")
        continue

    if puzzle.checkDone():
        print("solved!")
        break

    # Couldn't find any more actions to perform!
    print("Stuck!")
    break


puzzle.displayState().show()
