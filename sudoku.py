from random import shuffle
from copy import deepcopy


def make_assumptions(sudoku):
    for i, row in enumerate(sudoku):
        for j, value in enumerate(row):
            if not value:
                values = set(row) \
                         | set([sudoku[k][j] for k in range(9)]) \
                         | set([sudoku[m][n] for m in range((i // 3) * 3, (i // 3) * 3 + 3)
                                for n in range((j // 3) * 3, (j // 3) * 3 + 3)])
                yield i, j, list(set(range(1, 10)) - values)


def solve(sudoku):
    if all([k for row in sudoku for k in row]):
        return sudoku
    assumptions = list(make_assumptions(sudoku))
    shuffle(assumptions)
    x, y, values = min(assumptions, key=lambda x: len(x[2]))
    for v in values:
        new_sudoku = deepcopy(sudoku)
        new_sudoku[x][y] = v
        if s := solve(new_sudoku):
            return s
    return None


def solve_sudoku(text):
    return solve([list(map(int, i.strip())) for i in text.split('\n')])
