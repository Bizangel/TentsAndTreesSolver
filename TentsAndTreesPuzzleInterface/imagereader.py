import numpy as np
import matplotlib.pyplot as plt
import cv2
from TentsAndTreesPuzzleInterface.imagefetcher import FetchPuzzle

BACKGROUNDGREY = [230, 230, 230]
GRASSGREEN = [128, 255, 179]
TREEGREEN = [114, 247, 160]
TRUNKBROWN = [0, 102, 153]
LINEBLACK = [0, 0, 0]


def ParseImage(img_filename):
    original = cv2.imread(img_filename)

    [width, height, _] = np.shape(original)

    x = 0
    y = round(width/2)
    while True:
        if np.any(original[y, x] == LINEBLACK):
            leftborder = x
            break
        x += 1

    # line is always of length 1

    # go down
    x = leftborder
    y = round(width/2)
    while True:
        if not np.any(original[y, x] == LINEBLACK):
            bottomborder = y - 1
            break
        y += 1

    # go right
    x = leftborder
    y = bottomborder
    while True:
        if not np.any(original[y, x] == LINEBLACK):
            rightborder = x - 1
            break
        x += 1

    # go up
    x = leftborder
    y = round(width/2)
    while True:
        if not np.any(original[y, x] == LINEBLACK):
            topborder = y + 1
            break
        y -= 1

    y = topborder
    x = leftborder

    w = rightborder - leftborder
    h = bottomborder - topborder

    cropped = original[y: y+h, x: x+w]

    # Iterate through cropped image, identifying squares

    class SquareIdentifier:
        def __init__(self, img, treeval="tree", emptyval="empty"):
            self.x = 0  # coordinates in img
            self.y = 0

            self.height, self.width, _ = np.shape(img)
            self.img = img

            self.treeValue = treeval
            self.emptyval = emptyval

        def identifyRow(self):
            identified = []
            self.y += 2  # Ensure I'm inside a block/square.
            classified = False
            while True:

                self.x += 1  # iterate through
                if self.x == self.width - 1:
                    break
                if np.any(self.img[self.y, self.x] == BACKGROUNDGREY) and not classified:
                    classified = True
                    identified.append(self.emptyval)

                elif ((np.any(self.img[self.y, self.x] == BACKGROUNDGREY)) or
                      (np.any(self.img[self.y, self.x] == GRASSGREEN)) or
                      (np.any(self.img[self.y, self.x] == TRUNKBROWN))) and not classified:
                    classified = True
                    identified.append(self.treeValue)
                elif np.any(self.img[self.y, self.x] == LINEBLACK):
                    classified = False

            # print(identified)
            return identified

        def findNextRow(self):
            self.x = 0  # set x to 0
            self.x += 2  # now on a square
            while True:
                self.y += 1
                if self.y == self.height - 1:
                    return True  # Done
                if np.any(self.img[self.y, self.x] == LINEBLACK):
                    return False

        def identifyImage(self):
            stacks = []
            while True:
                stacks.append(self.identifyRow())
                if self.findNextRow():
                    break
            return np.row_stack(stacks)

    return SquareIdentifier(cropped, 1, 0).identifyImage()


def FetchAndParsePuzzle(filename):
    row, col = FetchPuzzle(filename)
    matrix = ParseImage(filename)
    return matrix, row, col
