class NFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states  # NFA states
        self.alphabet = alphabet  # Input alphabet
        self.transition_function = transition_function  # Transition function
        self.start_state = start_state  # Start state
        self.accept_states = accept_states  # Accept states

    def epsilon_closure(self, state):
        """
        Compute the epsilon closure of a given state.
        """
        stack = [state]  # Stack for states to process
        closure = set(stack)  # Set to store epsilon closure
        while stack:
            current_state = stack.pop()
            if current_state in self.transition_function and 'ε' in self.transition_function[current_state]:
                for next_state in self.transition_function[current_state]['ε']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def to_dfa(self):
        """
        Convert the NFA to a DFA.
        """
        dfa_states = {}  # Dictionary to store DFA states
        dfa_start_state = frozenset(self.epsilon_closure(self.start_state))  # DFA start state
        dfa_states[dfa_start_state] = {}  # Initialize DFA start state
        queue = [dfa_start_state]  # Queue for processing DFA states
        dfa_accept_states = set()  # Set to store DFA accept states
        while queue:
            current = queue.pop(0)  # Current DFA state
            if any(state in self.accept_states for state in current):
                dfa_accept_states.add(current)  # Mark as accept state if any NFA state is an accept state
            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue  # Skip epsilon transitions
                next_state = set()
                for state in current:
                    if state in self.transition_function and symbol in self.transition_function[state]:
                        for next_nfa_state in self.transition_function[state][symbol]:
                            next_state.update(self.epsilon_closure(next_nfa_state))
                next_state = frozenset(next_state)
                if next_state not in dfa_states:
                    queue.append(next_state)
                    dfa_states[next_state] = {}
                dfa_states[current][symbol] = next_state  # Record DFA transition
        return DFA(dfa_states, self.alphabet, dfa_start_state, dfa_accept_states)

class DFA:
    def __init__(self, states, alphabet, start_state, accept_states):
        self.states = states  # DFA states
        self.alphabet = alphabet  # Input alphabet
        self.start_state = start_state  # Start state
        self.accept_states = accept_states  # Accept states

    def __str__(self):
        """
        String representation of the DFA.
        """
        result = "States: " + str(list(self.states.keys())) + "\n"
        result += "Alphabet: " + str(self.alphabet) + "\n"
        result += "Start State: " + str(self.start_state) + "\n"
        result += "Accept States: " + str(list(self.accept_states)) + "\n"
        result += "Transitions:\n"
        for state, transitions in self.states.items():
            for symbol, next_state in transitions.items():
                result += "  " + str(state) + " -- " + symbol + " --> " + str(next_state) + "\n"
        return result

nfa = NFA(
    states={'p0', 'p1', 'p2'},
    alphabet={'a', 'b', 'ε'},
    transition_function={
        'p0': {'a': {'p0'}, 'ε': {'p1'}},
        'p1': {'b': {'p2'}}
    },
    start_state='p0',
    accept_states={'p2'}
)

dfa = nfa.to_dfa()
print(dfa)
