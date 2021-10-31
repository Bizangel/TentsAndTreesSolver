''' Sample '''
from TentsAndTreesPuzzleInterface.PuzzleStorage import StorePuzzle, LoadStoredPuzzle
from TentsAndTrees import TentsAndTrees, Player
import numpy as np
from logica import LPQuery, ASK

matrix, row, col = LoadStoredPuzzle("Puzzles/puzzle1.npz")
puzzle = TentsAndTrees(matrix, row, col)

myplayer = Player(puzzle)
myplayer.knowledge = LPQuery(
    myplayer.make_emptygreen_rule() + myplayer.make_unique_rule())

# myplayer.knowledge = LPQuery([])
# myplayer.knowledge = LPQuery(myplayer.make_unique_formulas())


def findFirstGreen():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                # play and reset
                if ASK(myplayer.cods.P([i, j, 3]), 'success', myplayer.knowledge):
                    # That square will no longer be empty.
                    myplayer.knowledge.unTELL(myplayer.cods.P([i, j, 0]))
                    puzzle.transition([i, j, 3])
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
    for value in range(4):
        queryval = ASK(
            myplayer.cods.P([i, j, value]), 'success', myplayer.knowledge)
        msg = "True" if queryval else "Unknown"
        print(
            f"Is there {TentsAndTrees.DisplayCodes[value]} in ({i},{j})?: {msg} ")

    # negations
    for value in range(4):
        queryval = ASK(
            '-' + myplayer.cods.P([i, j, value]), 'success', myplayer.knowledge)
        msg = "True" if queryval else "Unknown"
        print(
            f"Is there NOT {TentsAndTrees.DisplayCodes[value]} in ({i},{j})?: {msg} ")


puzzle.displayState().show()
while not puzzle.checkDone():
    myplayer.acknowledge_sight()
    start = puzzle.state

    if findFirstGreen():
        continue

    # Couldn't find any more actions to perform!
    print("Stuck!")
    break

puzzle.displayState().show()
