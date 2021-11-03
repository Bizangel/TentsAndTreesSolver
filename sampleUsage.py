''' Sample, Refer to Notebook'''
from TentsAndTreesPuzzleInterface.PuzzleStorage import LoadStoredPuzzle
from TentsAndTrees import TentsAndTrees, Player
from logica import LPQuery, pl_fc_ask

matrix, row, col = LoadStoredPuzzle("Puzzles/puzzle3.npz")
puzzle = TentsAndTrees(matrix, row, col)
myplayer = Player(puzzle)
myplayer.knowledge = LPQuery(
    myplayer.make_emptygreen_rule() +
    myplayer.make_unique_rule() +
    myplayer.make_emptyrowcol_rule() +
    myplayer.make_only_adjacent_tent_rule() +
    myplayer.make_emptygreen_adjacent_to_tent_rule() +
    myplayer.make_fill_remaining_tents_equal_rule() +
    myplayer.make_fillgreen_filledtents_row_rule()
)
myplayer.InitializeAtoms()
namerules = [rule.nombre for rule in myplayer.knowledge.reglas]
assert len(namerules) == len(set(namerules)), "There are duplicate rules!"


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
