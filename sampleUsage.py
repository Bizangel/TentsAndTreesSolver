''' Sample '''
from TentsAndTreesPuzzleInterface.PuzzleStorage import StorePuzzle, LoadStoredPuzzle
from TentsAndTrees import TentsAndTrees, Player
import numpy as np
from TentsAndTreesPuzzleInterface.imagereader import FetchAndParsePuzzle
from logica import LPQuery, ASK

# matrix, row, col = FetchAndParsePuzzle("Puzzles/puzzle4.png")
# StorePuzzle("Puzzles/puzzle4.npz", matrix, row, col)

matrix, row, col = LoadStoredPuzzle("Puzzles/puzzle3.npz")
puzzle = TentsAndTrees(matrix, row, col)


myplayer = Player(puzzle)

myplayer.knowledge = LPQuery(
    myplayer.make_emptygreen_rule() +
    myplayer.make_unique_rule() +
    myplayer.make_emptyrowcol_rule() +
    myplayer.make_zero_nonempty_rule() +
    myplayer.place_adjacent_tent_rule() +
    myplayer.make_emptygreen_adjacent_to_tent_rule()
)


def findFirstGreen():
    found = False
    for i in range(puzzle.m):
        for j in range(puzzle.n):
            if puzzle.state[i, j] == 0:  # only ask on empty squares
                # play and reset
                print(f"Asking --- {i} {j} ")
                if ASK(myplayer.cods.P([i, j, 3]), 'success', myplayer.knowledge):
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
                # play and reset
                if ASK(myplayer.cods.P([i, j, 2]), 'success', myplayer.knowledge):
                    # That square will no longer be empty.
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


def displayknowledge():

    print("The agent knows: ----------------")
    for dat in myplayer.knowledge.datos:
        # print(myplayer.knowledge.datos)
        try:
            print(myplayer.humanReadAtom(dat))
        except KeyError:
            continue
    print('-------------------------')


initial = np.array(myplayer.knowledge.datos)
while True:
    myplayer.acknowledge_sight()
    displayknowledge()
    # print("read")

    # print(initial == np.array(myplayer.knowledge.datos))
    if findFirstGreen():
        # print("Found Green")
        continue

    if findFirstTent():
        # print("Found Tent")
        continue

    # print("read")
    if puzzle.checkDone():
        print("solved!")
        break

    # Couldn't find any more actions to perform!
    print("Stuck!")
    break

# for i in range(8):
#     for j in range(8):
#         fullyAskTile(i, j)

puzzle.displayState().show()
