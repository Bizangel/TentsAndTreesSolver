from TreesAndTentsPuzzleInterface.imagereader import FetchAndParsePuzzle
from TreesAndTentsPuzzleInterface.imagedisplayer import DisplayPuzzle
from TreesAndTentsPuzzleInterface.PuzzleStorage import StorePuzzle, LoadStoredPuzzle

#  Fetch
# matrix, row, col = FetchAndParsePuzzle("Puzzles/puzzle2.png")
# StorePuzzle("Puzzles/puzzle2.npz", matrix, row, col)

# Read And Display

matrix, row, col = LoadStoredPuzzle("Puzzles/puzzle2.npz")
DisplayPuzzle(matrix, row, col).show()
