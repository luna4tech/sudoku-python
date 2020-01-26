import numpy as np
import random
from utils import constants


class SudokuSolver:
    steps = 0

    def isValid(self, grid, row_i, col_j, value):
        # check if row i has the value
        for i in range(constants.SIZE):
            if (not i == row_i) and (grid[i][col_j] == value):
                return False

        # check if column j has the value
        for j in range(constants.SIZE):
            if (not j == col_j) and (grid[row_i][j] == value):
                return False

        # check if subgrid has the value
        for i in range(constants.SUB_SIZE * int(row_i / constants.SUB_SIZE),
                       constants.SUB_SIZE * int(row_i / constants.SUB_SIZE) + 3):
            for j in range(constants.SUB_SIZE * int(col_j / constants.SUB_SIZE),
                           constants.SUB_SIZE * int(col_j / constants.SUB_SIZE) + 3):
                if (not (i == row_i and j == col_j)) and (grid[i][j] == value):
                    return False

        return True

    def solveSudokuInternal(self, inputGrid, output, i, j):
        count = 0
        if i >= constants.SIZE:
            for p in range(9):
                for q in range(9):
                    output[p][q] = inputGrid[p][q]
            return count + 1

        next_i = i if (j + 1) < constants.SIZE else (i + 1)
        next_j = (j + 1) if (j + 1) < constants.SIZE else 0

        if inputGrid[i][j] == 0:
            possibleValues = list(range(1, constants.SIZE + 1))
            random.shuffle(possibleValues)
            for k in possibleValues:
                if self.isValid(inputGrid, i, j, k):
                    inputGrid[i][j] = k
                    count = count + self.solveSudokuInternal(inputGrid, output, next_i, next_j)
                    if count >= 2:
                        break
                    self.steps = self.steps + 1
                    inputGrid[i][j] = 0  # backtrack

        else:
            count = count + self.solveSudokuInternal(inputGrid, output, next_i, next_j)

        return count

    def solveSudoku(self, inputGrid):
        self.steps = 0
        output = np.zeros([constants.SIZE, constants.SIZE], dtype=int)
        self.solveSudokuInternal(inputGrid, output, 0, 0)
        return output
