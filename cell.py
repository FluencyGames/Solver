import config


class Cell(object):

    def __init__(self, pos=-1, value=0, is_starter=False):
        self.values = [] if value == 0 else [value]
        self.locked = []
        self.pos = pos
        self.is_starter = is_starter
        self.candidates = config.PUZZLE_DEF['VALUES'].copy()

    def get_cell_name(self):
        row = self.pos // config.PUZZLE_DEF['NO_COLS']
        col = self.pos % config.PUZZLE_DEF['NO_COLS']
        return config.PUZZLE_DEF['ROW_NAMES'][row] + config.PUZZLE_DEF['COL_NAMES'][col]

    def get_num_candidates(self):
        return len(self.candidates)

    def get_candidates(self):
        return self.candidates

    def remove_candidate(self, value):
        self.candidates.remove(value)

    def is_solved(self):
        return len(self.values) == 1

    def get_value(self):
        if self.is_solved():
            return self.values[0]
        else:
            return 0

    def set_value(self, value):
        self.values = [value]

    def set_values(self, values):
        self.values = values.copy()
