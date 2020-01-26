import pygame

from graphics.cell_state_machine import Event, State
from utils import constants


# Represents each cell in sudoku grid
class InputBox:
    def __init__(self, rect, pos, fontSize, text=''):
        self.rect = rect
        self.pos = pos
        self.text = text
        self.font = pygame.font.Font(constants.FONT_TYPE, fontSize)
        self.txt_surface = self.font.render(text, True, constants.BLACK)
        self.sm = None
        self.smEvent = Event.NO_CLICK
        self.highlight = False

    def updateValue(self, sudokuGrid):
        sudokuGrid[self.pos[0]][self.pos[1]] = int(self.text)
        print(sudokuGrid)

    def clearValue(self, sudokuGrid):
        self.text = ''
        sudokuGrid[self.pos[0]][self.pos[1]] = 0
        print(sudokuGrid)

    # return event type based on input
    def validateInput(self, text, sudokuGrid, sudokuSolver):
        if text.isnumeric() and int(text) > 0:
            self.text = text
            if sudokuSolver.isValid(sudokuGrid, self.pos[0], self.pos[1], int(text)):
                return Event.CORRECT_INPUT
            else:
                return Event.WRONG_INPUT
        else:
            return Event.INVALID_INPUT

    def handle_event(self, event, sudokuGrid, sudokuSolver):
        # register mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.smEvent = Event.CLICK
            else:
                self.smEvent = Event.NO_CLICK if self.text == "" else self.validateInput(self.text, sudokuGrid,
                                                                                         sudokuSolver)

        # register value entered by user
        if (not self.sm.getCurrentState() == State.INPUT) and event.type == pygame.KEYDOWN and self.sm.getCurrentState() == State.ACTIVE:

            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                self.text = ""
                self.smEvent = Event.INVALID_INPUT
            else:
                self.smEvent = self.validateInput(event.unicode, sudokuGrid, sudokuSolver)

        self.sm.handleEvent(self.smEvent)

        # Re-render the text.
        self.txt_surface = self.font.render(self.text, True, constants.BLACK)

    def draw(self, screen):
        # draw empty rect with border
        pygame.draw.rect(screen, constants.BLACK, self.rect, constants.LINE_WIDTH)
        # draw rect filled with color based on current state
        pygame.draw.rect(screen, constants.STATUS[self.sm.getCurrentState().value], self.rect)
        if not self.sm.getCurrentState() is State.ACTIVE and self.highlight:
            pygame.draw.rect(screen, constants.YELLOW, self.rect)

        # draw the text.
        screen.blit(self.txt_surface, (self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2))
