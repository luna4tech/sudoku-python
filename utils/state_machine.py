class Function:
    def __init__(self, funcName, params):
        self.funcName = funcName
        self.params = params


class StateMachine:
    # states - list of enums or integers
    # transitions - list of list of enums or integers,
    #               each row represents event and
    #               each column represents current state
    #               cell value represents final state after the event occurs
    # handles - list of list of Function objects
    #               each row represents event and
    #               each column represents current state
    #               cell value represents the function to execute after the event occurs

    def __init__(self, current_state, states, transitions, handles):
        self.current_state = current_state
        self.states = states
        self.transitions = transitions
        self.handles = handles

    def handleEvent(self, event):
        # update new state based on event and current state
        new_state = self.transitions[event.value][self.current_state.value]
        # execute function based on event and current state
        handle = self.handles[event.value][self.current_state.value]
        if not handle is None:
            handle.funcName(handle.params)
        self.current_state = new_state if not new_state is None else self.current_state

    def getCurrentState(self):
        return self.current_state

    def setCurrentState(self, new_state):
        self.current_state = new_state
