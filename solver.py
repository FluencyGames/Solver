# parse the command line options
import getopt
import json
import sys

import urllib3 as url
from bs4 import BeautifulSoup
import puzzle

import settings
import config
import solve

puzzle_level = ''
puzzle_data = ''
definition_file = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], "l:q:p:d:", ["level", "puzzle", "quiet", "definition"])

except getopt.GetoptError:
    print('solver.py -level [easy | med | hard] -puzzle <puzzledata> -quiet -definition <configfile.json>')
    sys.exit(-1)

for opt, arg in opts:
    if opt == '-l':
        if arg == 'm' or arg == 'med' or arg == 'medium':
            puzzle_level = 'medium'
        elif arg == 'h' or arg == 'hard':
            puzzle_level = 'hard'
        else:
            puzzle_level = 'easy'
    elif opt == '-p' or opt == '--puzzle':
        puzzle_data = arg
    elif opt == '-q' or opt == '--quiet':
        settings.verbosity = -1
    elif opt == '-d' or opt == '--definition':
        definition_file = arg
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


def puzzle_from_string(data, structure):
    str = ''
    puz = []

    for c in data:
        if c == ' ':
            pass
        if c not in structure.puzzle_definition['VALUES']:
            puz.append(int(c))
        else:
            puz.append(0)

    if len(puz) != structure.puzzle_definition['NO_ROWS'] * structure.puzzle_definition['NO_COLS']:
        print('Error in puzzle data string.')
        return ''

    # print(puz)
    return puz

# create the puzzle object
pzle = puzzle.Puzzle()

# this is the definition of the puzzle structure
if settings.puzzle_definition == '':
    settings.puzzle_definition = config.PUZZLE_DEF
else:
    pass

# pull the puzzle data from NY Times site
if puzzle_data == '':
    puzzle_data = pull_puzzle(puzzle_level)
else:
    puzzle_data = puzzle_from_string(puzzle_data, settings)

# create the puzzle from the data
pzle.puzzle_create_from_data(puzzle_data, settings.puzzle_definition)


# for debugging
if settings.verbosity >= 0:
    # print the puzzle
    pzle.dump()

    # prompt user to solve
    response = input('Solve this puzzle (y/n)? ')
    if 'n' in response or 'N' in response:
        exit(0)


# check solution for correctness
ret = solve.solveit(pzle)
if ret:
    if settings.verbosity < 0:
        pzle.dump()
    if pzle.verify():
        print('Puzzle is complete!')
    else:
        print('Error in solution!')

print('Solver finished with return code {}'.format(ret))
