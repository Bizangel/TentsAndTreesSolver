import numpy as np


def StorePuzzle(filename, matrix, row, col):
    np.savez(filename, matrix=matrix, row=row, col=col)


def LoadStoredPuzzle(filename):
    data = np.load(filename)
    matrix = data["matrix"]
    row = data["row"]
    col = data["col"]
    return matrix, row, col
