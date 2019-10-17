class State(list):
    def __init__(self, values=None, empty_loc=None):
        """
        Matrix is a rectangular table of numerical values
        :param values:
        """
        self.shape = len(values), len(values[0])
        self.h, self.w = self.shape
        # self._validate_values(values)
        self.values = values
        self.pad = 1
        if self.shape[0] > 3:
            self.pad = 2
        if self.shape[0] > 10:
            self.pad = 3
        self.came_from = None
        self.dir_from = None
        if empty_loc is None:
            self._find_empty()
        else:
            self.empty_loc = empty_loc
        self.g = 0
    
    def _find_empty(self):
        found = False

        for i in range(self.h):
            for j in range(self.w):
                if self.values[i][j] == 0:
                    self.empty_loc = i, j
                    found = True
                if found:
                    break
            if found:
                break

    def _validate_values(self, values):
        """
        Validate list of lists to be of correct format
        :param values:
        :return:
        """
        prev_len = -1
        i = j = -1
        if values is None or len(values) == 0:
            self.shape = 0, 0
            return
        for i, row in enumerate(values):
            if prev_len == -1:
                prev_len = len(row)
            if prev_len != len(row):
                raise ValueError(f"Row {i} differs in length: {prev_len} != {len(row)}")
            for j, val in enumerate(row):
                if type(val) not in (int, float, complex):
                    raise ValueError(f"[{i}, {j}]: {val} is of bad type ({type(val)})")
                    if val == 0:
                        self.empty_loc = (i, j)
        if i == -1:
            self.shape = 0, 0
        else:
            self.shape = i + 1, j + 1

    def __repr__(self):
        if self.values:
            n = self.pad
            return '\n'.join([' '.join([str(c).rjust(n, ' ') for c in row]) for row in self.values])
        else:
            return str(self.values)
    
    def _swap(self, to):
        # self.empty_loc = to
        self[self.empty_loc], self[to] = self[to], self[self.empty_loc]
        self.empty_loc = to

    def swap(self, dir, inplace=False):
        y, x = self.empty_loc
        if dir == 'u' and y == 0 or dir == 'd' and y == self.h - 1:
            raise ValueError(f"{dir} cannot be performed")
        elif (dir == 'l' and x == 0) or (dir == 'r' and x == self.w - 1):
            raise ValueError(f"{dir} cannot be performed")
        if inplace:
            r = self
        else:
            r = self.copy()
        if dir == 'u':
            r._swap((y - 1, x))
        elif dir == 'r':
            r._swap((y, x + 1))
        elif dir == 'd':
            r._swap((y + 1, x))
        else:
            r._swap((y, x - 1))
        return r            

    def __getitem__(self, item):
        """
        A[key] -- access by indexing
        :param item:
        :return:
        """
        if type(item) is int:
            #  select row by default
            if self.shape[0] == 1:  # iterate by column if it's a row vector
                return self.values[0][item]
            elif self.shape[1] == 1:  # iterate by row if it's a column vector
                return self.values[item][0]
            return Matrix([self.values[item]])
        elif type(item) is list:
            return Matrix([self.values[i] for i in item])
        elif type(item) is tuple and len(item) == 2 and type(item[0]) is int and type(item[1]) is int:
            r, c = item
            return self.values[r][c]
        elif type(item) is slice:
            return Matrix(self.values[item])
        else:
            for i in item:
                if type(i) not in (int, slice):
                    raise ValueError(f"Bad index type {type(i)}")
            if len(item) != 2:
                raise ValueError(f"Don't understand index: {item}")
            if self.shape == (0, 0):
                return Matrix([[]])
            row_slice, col_slice = item
            rows = self.values[row_slice]  # M[0, :] to work
            if type(rows[0]) is not list:
                rows = [rows]
            subset = [row[col_slice] for row in rows]
            if type(subset) in (int, float, complex):
                return Matrix([[subset]])
            elif type(subset) in (list, tuple) and type(subset[0]) in (int, float, complex):
                return Matrix([subset])
            else:
                return Matrix(subset)

    def __setitem__(self, key, value):
        """
        A[key] = value
        :param key:
        :param value:
        :return:
        """
        if type(key) is int:
            row = key
            col = slice(None, None, None)
        else:
            row, col = key
        if type(row) is int:
            row_it = range(row, row + 1)
        else:
            row_it = range(*row.indices(len(self.values)))
        for r in row_it:
            if type(col) is int and hasattr(value, 'shape') and r < value.shape[1]:  # assigning values from Matrix-like object
                self.values[r][col] = value[r]
            elif type(col) is int and hasattr(value, 'shape') and value.shape == (1, 1):
                self.values[r][col] = value[0, 0]
            elif type(col) is int:
                self.values[r][col] = value
            else:
                for c in range(*col.indices(len(self.values[0]))):
                    self.values[r][c] = value[c]


    def copy(self):
        """ Return a copy of a state """
        return State([r[:] for r in self.values], empty_loc=self.empty_loc)

    def __eq__(self, o):
        return all([all([c1 == c2 for c1, c2 in zip(r1, r2)]) for r1, r2 in zip(self.values, o.values)])