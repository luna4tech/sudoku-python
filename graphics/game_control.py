import time

import pygame

from core.solver import SudokuSolver
from graphics.cell_state_machine import CellStateMachine, Event
from graphics.input_box import InputBox
from utils import constants
from utils.state_machine import Function


def formatTimer(time_spent_seconds):
    minutes = int(time_spent_seconds / 60)
    seconds = time_spent_seconds - int(time_spent_seconds / 60) * 60
    return "{:02d}:{:02d}".format(minutes, seconds)


def highlight(inputBoxes, sudokuGrid, text):
    if text.isnumeric() and int(text)>0:
        for i in range(constants.SIZE):
            for j in range(constants.SIZE):
                if sudokuGrid[i][j] == int(text):
                    inputBoxes[i][j].highlight = True
                else:
                    inputBoxes[i][j].highlight = False


class DisplaySudoku:
    def __init__(self, sudokuGrid, difficulty):
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT + constants.SCORE_BOARD))
        self.sudokuGrid = sudokuGrid
        self.difficulty = difficulty

    def drawGrid(self, size, thickness):
        for i in range(size):
            for j in range(size):
                width = constants.GRID_WIDTH / size
                height = constants.GRID_HEIGHT / size
                x = j * width
                y = i * height
                x_offset = (constants.SCREEN_WIDTH - constants.GRID_WIDTH) / 2
                y_offset = (constants.SCREEN_HEIGHT - constants.GRID_HEIGHT) / 2

                pygame.draw.rect(self.screen, constants.BLACK, (x + x_offset, y + y_offset, width, height), thickness)

    def createInputBox(self, i, j, cellValue):
        width = constants.GRID_WIDTH / constants.SIZE
        height = constants.GRID_HEIGHT / constants.SIZE
        x = j * width
        y = i * height
        x_offset = (constants.SCREEN_WIDTH - constants.GRID_WIDTH) / 2
        y_offset = (constants.SCREEN_HEIGHT - constants.GRID_HEIGHT) / 2

        if cellValue == 0:
            value = ""
            enable = True
        else:
            value = str(cellValue)
            enable = False
        # pygame x-axis is horizontal
        box = InputBox(pygame.Rect(x + x_offset, y + y_offset, width, height), (i, j), constants.NUMBERS_SIZE, value)
        box.sm = CellStateMachine.getStateMachine(enable, Function(box.updateValue, self.sudokuGrid), Function(box.clearValue, self.sudokuGrid))
        return box

    def displayTimer(self, start_ticks):
        x_offset = (constants.SCREEN_WIDTH - constants.GRID_WIDTH) / 2

        font = pygame.font.Font(constants.FONT_TYPE, constants.TIMER_SIZE)

        time_spent_seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)
        txt_surface = font.render(formatTimer(time_spent_seconds), True, constants.BLACK)
        self.screen.blit(txt_surface, (x_offset, constants.SCREEN_HEIGHT))

        return time_spent_seconds

    def displayLevel(self, difficulty):
        # difficulty Level
        x_offset = (constants.SCREEN_WIDTH - constants.GRID_WIDTH) / 2

        empty_star = pygame.image.load(constants.EMPTY_STAR_PATH)
        fill_star = pygame.image.load(constants.FILL_STAR_PATH)
        es_rect = empty_star.get_rect()
        fs_rect = fill_star.get_rect()

        for i in range(5 - difficulty):
            self.screen.blit(empty_star,
                             (constants.GRID_WIDTH + x_offset - (i + 1) * es_rect.w, constants.SCREEN_HEIGHT))
        for i in range(5 - difficulty, 5):
            self.screen.blit(fill_star,
                             (constants.GRID_WIDTH + x_offset - (i + 1) * fs_rect.w, constants.SCREEN_HEIGHT))

    def display_gameover(self, finish_time):
        font = pygame.font.Font(constants.FONT_TYPE, constants.MESSAGE_SIZE)

        messages = [constants.MESSAGE_SOLVED, constants.MESSAGE_CONTINUE, constants.MESSAGE_QUIT]
        for i in range(len(messages)):
            txt_surface = font.render(messages[i].format(formatTimer(finish_time)), True, constants.BLACK)
            self.screen.blit(txt_surface, ((constants.SCREEN_WIDTH - txt_surface.get_rect().w) / 2,
                                           txt_surface.get_rect().h * 2 * (i - int(len(messages) / 2)) + (
                                                   constants.SCREEN_HEIGHT - txt_surface.get_rect().h) / 2))

    def gameloop(self):
        inputBoxes = [[None for x in range(9)] for y in range(9)]
        for i in range(constants.SIZE):
            for j in range(constants.SIZE):
                inputBoxes[i][j] = self.createInputBox(i, j, self.sudokuGrid[i][j])

        start_ticks = pygame.time.get_ticks()
        finish_time = "00:00"

        running = True
        gameover = False

        while running:

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for box_row in inputBoxes:
                    for box in box_row:
                        box.handle_event(event, self.sudokuGrid, SudokuSolver())
                        if box.smEvent == Event.CLICK:
                            # highlight all boxes with that number
                            highlight(inputBoxes, self.sudokuGrid, box.text)
                if gameover and event.type == pygame.KEYDOWN:
                    return False if event.key == pygame.K_q else True

            self.screen.fill(constants.WHITE)

            # draw
            if gameover:
                self.display_gameover(finish_time)

            else:
                # grid
                for box_row in inputBoxes:
                    for box in box_row:
                        box.draw(self.screen)
                self.drawGrid(constants.SUB_SIZE, constants.BOLD_LINE_WIDTH)

                self.displayLevel(self.difficulty)
                finish_time = self.displayTimer(start_ticks)

                # check if grid is filled, then stop
                if (self.sudokuGrid > 0).all():
                    inputBoxes = []
                    gameover = True

            pygame.display.flip()
            time.sleep(0.1)
        return False
