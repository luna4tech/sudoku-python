from core.generator import SudokuGenerator
from graphics.game_control import DisplaySudoku
import pygame

pygame.init()

while True:
    generator = SudokuGenerator()
    sudokuGrid = generator.generateSudoku()
    difficulty = generator.difficulty(sudokuGrid)

    display = DisplaySudoku(sudokuGrid, difficulty)
    gamestate = display.gameloop()
    if not gamestate:
        pygame.quit()
        break