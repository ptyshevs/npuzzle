class State(object):
    def __init__(self, values=None):
        """
        Matrix is a rectangular table of numerical values
        :param values:
        """
        self.shape = None
        self.max_val = None
        self._validate_values(values)
        self.values = values

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
                if self.max_val is None or val > self.max_val:
                    self.max_val = val
        if i == -1:
            self.shape = 0, 0
        else:
            self.shape = i + 1, j + 1

    def __repr__(self):
        if self.values:
            n = len(str(self.max_val)) + 1 if self.max_val is not None else 1
            return '\n'.join([' '.join([str(c).rjust(n, '0') for c in row]) for row in self.values])
        else:
            return str(self.values)

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

    # def __add__(self, other):
    #     cpy = self.copy()
    #     if not hasattr(other, '__len__'):
    #         # assume other to be a single value, add to every element
    #         for i in range(self.shape[0]):
    #             for j in range(self.shape[1]):
    #                 cpy[i, j] += other
    #         return cpy
    #     elif self.shape != other.shape:
    #         raise ValueError(f"Add operation is defined for matrices of the same shape:"
    #                          f"{self.shape} != {other.shape}")
    #     for i in range(self.shape[0]):
    #         for j in range(self.shape[1]):
    #             cpy[i, j] += other[i, j]
    #     return cpy

    # def __radd__(self, other):
    #     return self.__add__(other)

    # def __rmul__(self, other):
    #     cpy = self.copy()
    #     for i in range(self.shape[0]):
    #         try:
    #             for j, v in zip(range(self.shape[1]), other):
    #                 cpy[i, j] *= v
    #         except TypeError:
    #             for j in range(self.shape[1]):
    #                 cpy[i, j] *= other
    #     return cpy

    def copy(self):
        """ Return a copy of a state """
        return State([[self[i, j] for j in range(self.shape[1])] for i in range(self.shape[0])])

    # def __mul__(self, other):
    #     return self.__rmul__(other)

    # def __sub__(self, other):
    #     return self.__add__(-other)

    # def __truediv__(self, other):
    #     cpy = self.copy()
    #     for i in range(self.shape[0]):
    #         try:
    #             for j, v in zip(range(self.shape[1]), other):
    #                 if hasattr(v, '__len__'):
    #                     cpy[i, j] /= v[j]
    #                 else:
    #                     cpy[i, j] /= v
    #         except TypeError:
    #             for j in range(self.shape[1]):
    #                 cpy[i, j] /= other
    #     return cpy

    # def __neg__(self):
    #     cpy = self.copy()
    #     for i in range(self.shape[0]):
    #         for j in range(self.shape[1]):
    #             cpy[i, j] = -cpy[i, j]
    #     return cpy

    # def round(self, v=0):
    #     """
    #     Round every element of a matrix up to <v> places
    #     :param v:
    #     :return:
    #     """
    #     cpy = self.copy()
    #     for i in range(self.shape[0]):
    #         for j in range(self.shape[1]):
    #             cpy[i, j] = round(cpy[i, j], v)
    #     return cpy

    # def __eq__(self, other):
    #     """
    #     Expecting other of the same shape
    #     :param other:
    #     :return:
    #     """
    #     try:
    #         if self.shape != other.shape:
    #             return False
    #         for i in range(self.shape[0]):
    #             for j in range(self.shape[1]):
    #                 if self[i, j] != other[i, j]:
    #                     return False
    #         return True
    #     except (AttributeError, IndexError):
    #         pass
    #     # assume other is a single value
    #     for i in range(self.shape[0]):
    #         for j in range(self.shape[1]):
    #             if self[i, j] != other:
    #                 return False
    #     return True

    # def __pow__(self, power, modulo=None):
    #     cpy = self.copy()
    #     for i in range(cpy.shape[0]):
    #         for j in range(cpy.shape[1]):
    #             cpy[i, j] = pow(cpy[i, j], power, modulo)
    #     return cpy

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def max(self):
    #     """
    #     Return maximum value in the Matrix
    #     :return: maximum value
    #     """
    #     return max([max(row) for row in self])

    # @property
    # def T(self):
    #     """
    #     Matrix transpose: interchange rows and columns
    #     :return: transposed Matrix
    #     """
    #     return Matrix([[self[i, j] for i in range(self.shape[0])] for j in range(self.shape[1])])

    # def __matmul__(self, other):
    #     """ [vector|matrix] multiplication """
    #     if self.shape[1] != other.shape[0]:
    #         raise IndexError(f"Dimensions must match: {self.shape} and {other.shape}")
    #     r = Matrix([[0 for _ in range(other.shape[1])] for _ in range(self.shape[0])])
    #     for i, row in enumerate(self.values):
    #         for j, col in enumerate(other.T.values):
    #             r[i, j] = sum([r * c for r, c in zip(row, col)])
    #     return r

    # def __len__(self):
    #     return self.shape[0]

    # def is_close(self, other):
    #     """ Check if all entries are equal (controlling for floating-point errors) """
    #     if self.shape != other.shape:
    #         raise IndexError(f"Dimensions must match: {self.shape} and {other.shape}")
    #     for i in range(self.shape[0]):
    #         for j in range(self.shape[1]):
    #             if not self._is_close(self[i, j], other[i, j]):
    #                 return False
    #     return True

    # def _is_close(self, a, b, tol=1e-9):
    #     """ Compare two floating-point numbers """
    #     return abs(a - b) <= tol

    # def norm(self, norm=1):
    #     """
    #     Calculate matrix norm
    #     :param norm: which norm to calculate
    #     :return:
    #     """
    #     if norm == 1:
    #         return max([sum([abs(_) for _ in self[:, j]]) for j in range(self.shape[1])])
    #     elif norm == float('inf'):
    #         return max([sum([abs(_) for _ in self[i, :]]) for i in range(self.shape[0])])
    #     elif norm == 2 and (self.shape[0] == 1 or self.shape[1] == 1):
    #         return self._euclidean_norm()
    #     elif norm == 'frobenius':
    #         return self._frobenius_norm()
    #     else:
    #         raise NotImplementedError(f"{norm}-norm is not implemented!")

    # def trace(self):
    #     n = min(self.shape[0], self.shape[1])
    #     return sum([self[_, _] for _ in range(n)])

    # def _euclidean_norm(self):
    #     if self.shape[0] == 1:
    #         return sum(self[0, :] ** 2) ** 0.5
    #     elif self.shape[1] == 1:
    #         return sum(self[:, 0] ** 2) ** 0.5

    # def _frobenius_norm(self, vectorized=True):
    #     if vectorized:
    #         return (self @ self.T).trace() ** 0.5
    #     else:
    #         return sum([sum([self[i, j] ** 2 for j in range(self.shape[1])]) for i in range(self.shape[0])]) ** 0.5
