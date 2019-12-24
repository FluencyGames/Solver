# parse the command line options
import getopt
import json
import sys

import urllib3 as url
from bs4 import BeautifulSoup
import puzzle

import config
import solve

puzzle_level = 'easy'

try:
    opts, args = getopt.getopt(sys.argv[1:], "emh", ["easy", "med", "hard"])

except getopt.GetoptError:
    print('solver.py [easy] [med] [hard]')
    sys.exit(-1)

for arg in args:
    if arg == 'm' or arg == 'med' or arg == 'medium':
        puzzle_level = 'medium'
    elif arg == 'h' or arg == 'hard':
        puzzle_level = 'hard'
    else:
        pass


def pull_puzzle(level):
    urlstring = 'https://www.nytimes.com/puzzles/sudoku/' + level

    http = url.PoolManager()
    page = http.request('GET', urlstring)

    soup = BeautifulSoup(page.data, 'html.parser')

    # print(soup.find_all("div", class_='pz-game-screen'))
    game_data = soup.find("script")
    text = game_data.text.lstrip('window.gameData = ')

    jdata = json.loads(text)

    puzzle = jdata[level]['puzzle_data']['puzzle']

    return puzzle


def verify_solved_puzzle():
    return True

def dump(data):
    index = 0
    str = ''

    for r in range(config.PUZZLE_DEF["NO_ROWS"]):
        for c in range(config.PUZZLE_DEF["NO_COLS"]):
            if puzzle_data[index] != 0:
                str += ' {} '.format(data[index])
            else:
                str += '   '
            index += 1
            if c == 2 or c == 5:
                str += ' | '
        print(str)
        if r == 2 or r == 5:
            print("-" * 33)
        str = ''


# pull the puzzle data from NY Times site
puzzle_data = pull_puzzle(puzzle_level)

# create the puzzle object
pzle = puzzle.Puzzle()
pzle.puzzle_create_from_data(puzzle_data)

# for debugging
pzle.dump()

# prompt user to solve
response = input('Solve this puzzle (y/n)? ')
if 'n' in response or 'N' in response:
    exit(0)

# add regions
for collection in config.PUZZLE_DEF['COLLECTIONS']:
    region_def = config.PUZZLE_DEF[collection]

    for r in region_def:
        pzle.puzzle_add_region(collection, r)

# check solution for correctness
ret = solve.solveit(pzle)
if ret:
    if pzle.verify():
        print('Puzzle is complete!')
    else:
        print('Error in solution!')

print('Solver finished with return code {}'.format(ret))






