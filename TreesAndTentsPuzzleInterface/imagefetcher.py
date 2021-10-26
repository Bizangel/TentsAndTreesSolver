import base64
from selenium import webdriver
from time import sleep
from pathlib import Path

'''
PUZZLES ARE TAKEN FROM 
===================================================================
"https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html"
===================================================================

All credits of puzzle generation go to their respective authors.

The downloading and fetching of said puzzles is only done for educational purpooses.
'''


def FetchPuzzle(filename):
    chromedriver_path = str(
        (Path(__file__).resolve().parent / "chromedriver.exe"))
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(
        "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/tents.html")

    sleep(15)
    canvas = driver.find_element_by_css_selector("#puzzlecanvas")

    ele = driver.find_element_by_css_selector("#permalink-desc")
    x = ele.get_attribute("href")
    index = x.find(",")
    numbers = x[index+1:]
    total = numbers.split(',')

    col = total[:len(total)//2]
    row = total[len(total)//2:]
    # get the canvas as a PNG base64 string
    canvas_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas)

    # decode
    canvas_png = base64.b64decode(canvas_base64)

    # save to a file
    with open(filename, 'wb') as f:
        f.write(canvas_png)

    driver.close()

    return row, col
