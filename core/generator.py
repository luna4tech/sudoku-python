from utils import constants
import numpy as np
import random
from core.solver import SudokuSolver


class SudokuGenerator:
    solver = SudokuSolver()

    def generateSudoku(self):
        grid = np.zeros([constants.SIZE, constants.SIZE], dtype=int)

        # generate a random solved sudoku grid
        solvedGrid = self.solver.solveSudoku(grid)
        # print(solvedGrid)

        # remove K random values
        indices = list(range(constants.SIZE * constants.SIZE))
        random.shuffle(indices)

        while True:
            index = indices.pop()
            # find row and column index based on array index (0-80)
            i = int(index / constants.SIZE)
            j = index - constants.SIZE * i

            removedValue = solvedGrid[i][j]
            solvedGrid[i][j] = 0

            input = np.copy(solvedGrid)
            output = np.zeros([constants.SIZE, constants.SIZE], dtype=int)

            # remove values until duplicate solutions is found
            if self.solver.solveSudokuInternal(input, output, 0, 0) >= 2:
                solvedGrid[i][j] = removedValue  # restore the removed value
                break

        return solvedGrid

    def difficulty(self, unsolvedSudokuBoard):
        self.solver.solveSudoku(unsolvedSudokuBoard)
        return int(self.solver.steps / 500) + 1
