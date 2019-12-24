import config
import puzzle
import cell
import settings


def report(text, vb=None):
    verbosity = settings.verbosity if vb is None else vb
    if verbosity >= 0:
        print(text)


def debug(text):
    if settings.debug:
        print(text)


def set_all_candidates(pz):
    for c in pz.cells:
        removed = []

        if not c.is_solved():
            # find all regions this cell belongs to
            regions = pz.get_regions_from_cell(c.pos)
            # print('Cell {}: {}'.format(c.pos, regions))

            for r in regions:
                # if we have only 1 candidate left,
                # the cell is solved!
                if c.get_num_candidates() == 1:
                    break;

                # print(r)
                for pos in r:
                    cel = pz.get_cell_from_position(pos)
                    if cel.is_solved():
                        if cel.get_value() in c.get_candidates():
                            c.remove_candidate(cel.get_value())
                            removed.append(cel.get_value())

            # print("Cell {}: Removed {}".format(c.get_cell_name(), removed))
            # print("Cell candidiates: {}".format(c.get_candidates()))


# depreciated folded into find_singles
def find_naked_singles(pzle):
    report('Looking for Naked Singles...')
    dirty = False

    for c in pzle.cells:
        if not c.is_solved() and c.get_num_candidates() == 1:
            c.set_value(c.get_candidates()[0])
            report('Setting Cell {} to {}'.format(c.get_cell_name(), c.get_value()))
            dirty = True
    return dirty


def find_singles(pzle):
    # find values that only appear once in a region
    report('Looking for Naked/Hidden Singles...')
    dirty = False

    collections = pzle.regions.keys()
    for collection in collections:
        for region in pzle.regions[collection]:

            # this is the map of values --> [ cell positions ]
            pos_candidates = {}

            # for each cell position in our region, get
            # the candidates and map to the position
            for cell_position in region:
                cel = pzle.get_cell_from_position(cell_position)
                if not cel.is_solved():
                    for v in cel.get_candidates():
                        map_value_to_cell_position(pos_candidates, v, cell_position)

            # check each value to see if a number has only 1 valid cell
            # print(pos_candidates)
            for pos in pos_candidates:
                for v, pos in pos_candidates.items():
                    if len(pos) == 1:
                        cel = pzle.get_cell_from_position(pos[0])
                        cel.set_value(v)
                        report('Setting Cell {} to {}'.format(cel.get_cell_name(), v))
                        # dirty = True
                        return True

    return dirty


def map_value_to_cell_position(dict, v, pos):
    if dict.get(v) is None:
        dict[v] = []
    dict[v].append(pos)


def remove_candidates_from_region(pzle, r, candidates, locked_positions):
    dirty = False
    for pos in r:
        if pos not in locked_positions:
            c = pzle.get_cell_from_position(pos)
            if not c.is_solved():
                for v in candidates:
                    if v in c.candidates:
                        report('Remove {} from cell {}'.format(v, c.get_cell_name()))
                        c.candidates.remove(v)
                        dirty = True
    return dirty


def remove_candidates_from_cells(pzle, values, positions):
    dirty = False
    for pos in positions:
        cel = pzle.get_cell_from_position(pos)
        for value in values:
            if value in cel.candidates:
                report('Remove {} from cell {}'.format(value, cel.get_cell_name()))
                cel.candidates.remove(value)
                dirty = True

    return dirty


def find_naked_doubles(pzle):
    report('Looking for Naked Doubles...')
    dirty = False
    cell_doubles = []

    for cel in pzle.cells:
        if not cel.is_solved() and cel.get_num_candidates() == 2:
            cell_doubles.append(cel)

    c1 = cell_doubles.pop()
    while len(cell_doubles) != 0:
        for c2 in cell_doubles:
            if c1.candidates == c2.candidates:
                regions = pzle.get_common_regions_from_cells([c1.pos, c2.pos])

                # if regions is not an empty set (list), then we have common
                # regions to remove doubles
                debug('Common regions between {} and {}: {}'.format(c1.get_cell_name(),
                                                                    c2.get_cell_name(),
                                                                    regions))
                if len(regions) != 0:
                    for r in regions:
                        if remove_candidates_from_region(pzle, r, c1.candidates, [c1.pos, c2.pos]):
                            dirty = True
        c1 = cell_doubles.pop()

    return dirty


def find_doubles(pzle):
    report('Looking for Naked Doubles...')
    dirty = False

    collections = pzle.regions.keys()
    for collection in collections:
        for region in pzle.regions[collection]:

            # this is the map of values --> [ cell positions ]
            pos_candidates = {}

            # for each cell position in our region, get
            # the candidates and map to the position
            for cell_position in region:
                cel = pzle.get_cell_from_position(cell_position)
                if not cel.is_solved():
                    for v in cel.get_candidates():
                        map_value_to_cell_position(pos_candidates, v, cell_position)

            # this should contain the entire map
            # print(pos_candidates)

            # iterate through our map, pulling out the value-pos pairs
            for v, pos1 in pos_candidates.items():
                if len(pos1) == 2:

                    # find all the values that have the same candidates as this value
                    values = [val for val, p in pos_candidates.items() if p == pos1]

                    # we should have 2 values for this length
                    if len(values) == 2:
                        regions = pzle.get_common_regions_from_cells(pos1)
                        # print(regions)

                        # we should always have valid regions here...
                        if len(regions) != 0:
                            for r in regions:
                                if remove_candidates_from_region(pzle, r, values, pos1):
                                    dirty = True
                                other_values = [val for val in pzle.get_puzzle_values() if val not in values]
                                print('Positions: {}'.format(pos1))
                                print('Other Values: {}'.format(other_values))
                                if remove_candidates_from_cells(pzle, other_values, pos1):
                                    dirty = True
    return dirty


def find_triples(pzle):
    report('Looking for Naked Triples...')
    dirty = False

    collections = pzle.regions.keys()
    for collection in collections:
        print(collection)
        for region in pzle.regions[collection]:

            # this is the map of values --> [ cell positions ]
            pos_candidates = {}
            for cell_position in region:
                # for each cell position in our region, get
                # the candidates and map to the position
                cel = pzle.get_cell_from_position(cell_position)
                if not cel.is_solved():
                    for v in cel.get_candidates():
                        map_value_to_cell_position(pos_candidates, v, cell_position)
            # this should contain the entire map
            print(pos_candidates)

            # iterate through our map, pulling out the value-pos pairs
            for v, pos1 in pos_candidates.items():
                if len(pos1) == 3:
                    debug('value: {}, pos1: {}'.format(v, pos1))

                    # find all the values that have the same candidates as this value
                    # values = [val for val, p in pos_candidates.items() if p == pos1]
                    values = [val for val, p in pos_candidates.items() if set(p).issubset(pos1)]
                    debug('Values: {}'.format(values))

                    # we should have 2 values for this length
                    if len(values) == 3:
                        regions = pzle.get_common_regions_from_cells(pos1)
                        for r in regions:
                            if remove_candidates_from_region(pzle, r, values, pos1):
                                dirty = True
                            other_values = [val for val in pzle.get_puzzle_values() if val not in values]
                            debug('Positions: {}'.format(pos1))
                            debug('Other Values: {}'.format(other_values))
                            if remove_candidates_from_cells(pzle, other_values, pos1):
                                dirty = True

    return dirty


def solveit(pzle):
    algorithms = [
        find_singles,
        find_doubles,
        find_triples
    ]

    while True:
        set_all_candidates(pzle)
        for alg in algorithms:
            dirty = alg(pzle)
            if dirty:
                if settings.verbosity > 0:
                    pzle.dump()
                break
            else:
                if settings.verbosity > 0:
                    resp = input('Continue (y/n)? ')
                    if 'n' in resp or 'N' in resp:
                        return -1

        if pzle.is_solved():
            return 1
