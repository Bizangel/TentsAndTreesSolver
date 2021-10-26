from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from cv2 import line
import numpy as np
from TreesAndTentsPuzzleInterface.imagereader import ParseImage
from pathlib import Path


def generateImageGrid(indexmatrix, indeximages, gridlength, backgroundcol='white'):
    '''Takes a numpy indexmatrix of integers
    and generates a grid, where each square is the
    image of corresponding index in indeximages

    Example:
    indexmatrix = [0, 1, 0, 1
                   0, 1, 0, 1]
    indeximages = [<PIL.Image>,<PIL.Image>]

    Then we get a 2x4 grid where the images are located accordingly
    '''
    linecolor = "#000000"
    m, n = np.shape(indexmatrix)
    width = gridlength*m + (m+1)
    height = gridlength*n + (n+1)
    # img_w, img_h = indeximages.size
    background = Image.new('RGBA', (width, height), (230, 230, 230, 255))
    img1 = ImageDraw.Draw(background)

    for i in range(m + 1):
        img1.line((i*gridlength + i, 0, i*gridlength + i, height),
                  fill=linecolor, width=0)
        img1.line((0, i*gridlength + i, width, i*gridlength + i),
                  fill=linecolor, width=0)

    toplace = [image.resize((gridlength, gridlength)) for image in indeximages]
    for i in range(m):
        for j in range(n):
            background.paste(toplace[indexmatrix[j, i]],
                             (i*gridlength+i + 1,
                              j*gridlength+j+1), toplace[indexmatrix[j, i]])
    # background.show()
    return background


def addRowColNumbers(img, row, col):
    '''Adds necessary tents column and rows numbers'''
    tablewidth, tableheight = img.size
    squaresize = round(tablewidth/len(row))
    fullimg = Image.new('RGBA', (tablewidth + squaresize * 2,
                                 tableheight + squaresize*2),
                        (255, 255, 255, 255))
    fullimg.paste(img, (0, 0), img)
    draw = ImageDraw.Draw(fullimg)
    myfont = ImageFont.truetype(
        str(Path(__file__).resolve().parent / "Roboto-Regular.ttf"), round(squaresize/2))

    for i in range(len(col)):
        draw.text((round((2*i+1)*squaresize/2 - squaresize/4),
                   tableheight + squaresize/4),
                  str(col[i]),
                  font=myfont, fill=(0, 0, 0, 255))
    for i in range(len(row)):
        draw.text((tablewidth + squaresize/4,
                   (round((2*i+1)*squaresize/2 - squaresize/4))
                   ),
                  #   str(row[len(row) - i - 1]),
                  str(row[i]),
                  font=myfont, fill=(0, 0, 0, 255))
    return fullimg


def DisplayPuzzle(matrix, row, col):

    empty = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    tree = Image.open(str(Path(__file__).resolve().parent / "tree.png"))
    tent = Image.open(str(Path(__file__).resolve().parent / "tent.png"))
    table = generateImageGrid(matrix, [
        empty, tree, tent], 60)
    return addRowColNumbers(table, row, col)
