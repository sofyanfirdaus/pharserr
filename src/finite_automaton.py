class FiniteAutomaton:

    def __init__(self,
                 init_state: str,
                 final_state: str,
                 transitions: dict[str, dict[str, str]] = {}):
        self.states = set(transitions.keys())
        self.states.add(init_state)
        self.states.add(final_state)

        self.transitions = transitions
        self.transitions.setdefault(init_state, {})
        self.transitions.setdefault(final_state, {})

        self.init_state = init_state
        self.final_state = final_state

    def set_init_state(self, init_state: str):
        self.init_state = init_state

    def set_final_state(self, final_state: str):
        self.final_state = final_state

    def add_transitions(self, state: str, transisiton: dict[str, str]):
        self.states.add(state)
        self.transitions.setdefault(state, {})
        self.transitions[state].update(transisiton)

    def add_transition(self, state: str, events: str, next_state: str):
        self.states.add(state)
        self.transitions.setdefault(state, {})
        for event in events:
            self.transitions[state].update({event: next_state})

    def next_state(self, cur_state: str, event: str) -> str:
        return self.transitions[cur_state].get(event, "nil")

    def evaluate(self, string: str) -> tuple[bool, str]:
        cur_state = self.init_state
        for event in string:
            cur_state = self.next_state(cur_state, event)
            if cur_state == "nil":
                break
        return (cur_state == self.final_state, cur_state)


ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"

automaton = FiniteAutomaton("q0", "q2")
automaton.add_transition("q0", ALPHABET + "_", "q1")
automaton.add_transition("q1", ALPHABET + "_" + NUMBERS, "q2")
automaton.add_transition("q2", ALPHABET + "_" + NUMBERS, "q2")

accepted, state = automaton.evaluate("Variabel")

print(accepted)
