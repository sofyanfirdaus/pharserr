class FiniteAutomaton:
    def __init__(
        self,
        init_state: str,
        final_states: set[str],
        transitions: dict[str, dict[str, str]] = {},
    ):
        self.states = set(transitions.keys())
        self.states.add(init_state)
        for state in final_states:
            self.states.add(state)

        self.transitions = transitions
        self.transitions.setdefault(init_state, {})
        for state in final_states:
            self.transitions.setdefault(state, {})

        self.init_state = init_state
        self.final_states = final_states

    def set_init_state(self, init_state: str):
        self.init_state = init_state

    def add_final_states(self, state: str):
        self.final_states.add(state)

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
        return (cur_state in self.final_states, cur_state)


class IdentifierAutomaton:
    def __init__(self):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        self.automaton = FiniteAutomaton("q0", {"q0", "q1"})
        self.automaton.add_transition("q0", alphabet + "_", "q1")
        self.automaton.add_transition("q1", alphabet + "_" + numbers, "q2")
        self.automaton.add_transition("q2", alphabet + "_" + numbers, "q2")

    def validate(self, string: str) -> bool:
        acc, _ = self.automaton.evaluate(string)
        return acc
