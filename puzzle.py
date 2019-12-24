import config
import cell


class Puzzle(object):

    def __init__(self):
        self.data = []
        self.cells = []
        self.values = []
        self.regions = {}
        self.definition = config.PUZZLE_DEF

    def puzzle_define_regions(self):
        # add regions
        for collection in self.definition['COLLECTIONS']:
            region_def = self.definition[collection]

            for r in region_def:
                self.puzzle_add_region(collection, r)

    def puzzle_create_from_data(self, data, definition=config.PUZZLE_DEF):
        index = 0
        self.definition = definition
        self.data = data.copy()
        self.values = definition["VALUES"]
        for r in range(definition["NO_ROWS"]):
            for c in range(definition["NO_COLS"]):
                self.cells.append(cell.Cell(index, data[index], data[index] != 0))
                index += 1
        self.puzzle_define_regions()

    def puzzle_add_region(self, collection, region_def):
        if collection not in self.regions:
            self.regions[collection] = []
        self.regions[collection].append(region_def)

    def get_puzzle_values(self):
        return self.values.copy()

    def get_cell_from_position(self, pos):
        return self.cells[pos]

    def is_solved(self):
        for c in self.cells:
            if not c.is_solved():
                return False

        return True

    def verify(self):
        # verify if there are no conflicts
        for collection in self.regions.keys():
            for region in self.regions[collection]:
                values = []
                for pos in region:
                    if self.get_cell_from_position(pos).is_solved():
                        v = self.get_value_at_pos(pos)
                        if v in values:
                            return False
                        else:
                            values.append(v)
        return True

    def get_regions_from_cell(self, pos):
        regions = []
        for collection in self.regions.keys():
            for r in self.regions[collection]:
                if pos in r:
                    regions.append(r)
                    break

        return regions

    def get_common_regions_from_cells(self, positions):
        regions = []
        for p in positions:
            regions.append(self.get_regions_from_cell(p))
        r = regions.pop()
        while len(regions) != 0:
            r2 = regions.pop()
            r = [item for item in r if item in r2]
        return r

    def get_value_at_pos(self, pos):
        return self.get_cell_from_position(pos).get_value()

    def set_pos_to_value(self, pos, v):
        cel = self.get_cell_from_position(pos)
        if cel.is_solved():
            print('Error: Trying to set cell {} to value {} when already solved!'.format(cel.get_cell_name(), v))
        else:
            cel.set_value(v)

    def dump(self):
        index = 0

        # print(self.data)
        # print('='*33)

        txt = '   '
        for r in config.PUZZLE_DEF["COL_NAMES"]:
            txt += ' {} '.format(r)
            if r == '3' or r == '6':
                txt += ' '

        print(txt)
        print('   ' + '-'*30)

        for r in range(config.PUZZLE_DEF["NO_ROWS"]):
            txt = '{} |'.format(config.PUZZLE_DEF["ROW_NAMES"][r])
            for c in range(config.PUZZLE_DEF["NO_COLS"]):
                cl = self.cells[index]
                if cl.is_solved():
                    txt += ' {} '.format(cl.get_value())
                else:
                    txt += '   '
                index += 1
                if c == 2 or c == 5:
                    txt += '|'
                if c == 8:
                    txt += ' |'
            print(txt)
            if r == 2 or r == 5 or r == 8:
                print('   ' + '-' * 30)


