from enum import Enum

from utils.state_machine import StateMachine


class State(Enum):
    INPUT = 0
    INACTIVE = 1
    ACTIVE = 2
    ERROR = 3


class Event(Enum):
    CLICK = 0
    NO_CLICK = 1
    CORRECT_INPUT = 2
    WRONG_INPUT = 3
    INVALID_INPUT = 4


class CellStateMachine:
    # each cell maintains its own state machine
    # enable -> if the cell is enabled for user input
    def __init__(self):
        pass

    @staticmethod
    def getStateMachine(enable, updateValueFunc, clearValueFunc):
        transitions = [[State.INPUT, State.ACTIVE, State.ACTIVE, State.ACTIVE],  # CLICK
                       [State.INPUT, State.INACTIVE, State.INACTIVE, State.ERROR],  # NO_CLICK
                       [None, None, State.INACTIVE, None],  # CORRECT_INPUT
                       [None, None, State.ERROR, None],  # WRONG_INPUT
                       [None, None, State.INACTIVE, None]]  # INVALID_INPUT
        handles = [[None, None, None, None],  # CLICK
                   [None, None, None, None],  # NO_CLICK
                   [None, None, updateValueFunc, None],  # CORRECT_INPUT
                   [None, None, updateValueFunc, None],  # WRONG_INPUT
                   [None, None, None, None]]  # INVALID_INPUT

        states = [State.INPUT, State.INACTIVE, State.ACTIVE, State.ERROR]

        return StateMachine(State.INACTIVE if enable else State.INPUT, states, transitions, handles)
