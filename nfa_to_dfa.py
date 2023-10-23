class NFAtoDFA:
    def __init__(self, nfa_states, alphabet, nfa_transitions, nfa_start, nfa_accept):
        self.nfa_states = nfa_states
        self.alphabet = alphabet
        self.nfa_transitions = nfa_transitions
        self.nfa_start = nfa_start
        self.nfa_accept = nfa_accept

        self.dfa_states = set()
        self.dfa_transitions = {}
        self.dfa_start = set()
        self.dfa_accept = set()


    def move(self, states, symbol):
        result = set()
        for state in states:
            if symbol in self.nfa_transitions[state]:
                result.update(self.nfa_transitions[state][symbol])
        return result

    def convert(self):
        queue = [self.nfa_start]
        visited = set()

        while queue:
            current_states = queue.pop()
            #  получаем из очереди последний посещенный узел(-ы)НФА и добавляем к вершинам ДКА
            self.dfa_states.add(tuple(sorted(list(current_states))))
            visited.add(tuple(sorted(list(current_states))))

            #  если текущее состояние в НФА является терминальным, то и в ДФА тоже будет терминальным
            if any(state in self.nfa_accept for state in current_states):
                self.dfa_accept.add(tuple(sorted(list(current_states))))

            for symbol in self.alphabet:
                next_states = self.move(current_states, symbol)
                if tuple(sorted(list(next_states))) not in visited:
                    queue.append(next_states)

        self.dfa_start = tuple(sorted(list(self.nfa_start)))

        for dfa_state in self.dfa_states:
            dfa_state_set = set(dfa_state)
            self.dfa_transitions[dfa_state] = {}
            for symbol in self.alphabet:
                next_states = self.move(dfa_state_set, symbol)
                self.dfa_transitions[dfa_state][symbol] = tuple(sorted(list(next_states)))

    def display_dfa(self):
        print("DFA States:")
        for state in self.dfa_states:
            print(state)
        print("DFA Transitions:")
        for state, transitions in self.dfa_transitions.items():
            print(f"{state} -> {transitions}")
        print("DFA Start State:")
        print(self.dfa_start)
        print("DFA Accept States:")
        for state in self.dfa_accept:
            print(state)




nfa_states = {'S', 'D', 'f'}
alphabet = {'a', 'b', '0'}
nfa_transitions = {
    'S': {'a': {'f', 'D'}, 'b': {'D'}},
    'D': {'0': {'D', 'f'}},
    'f': {}
}
nfa_start = 'S'
nfa_accept = {'f'}

converter = NFAtoDFA(nfa_states, alphabet, nfa_transitions, nfa_start, nfa_accept)
converter.convert()
converter.display_dfa()


def check_string(dfa, input_string):
    current_state = dfa.dfa_start  # Начнем с начального состояния
    for symbol in input_string:
        if symbol not in dfa.alphabet:
            return False  # Символ не входит в алфавит DFA
        next_state = dfa.dfa_transitions[current_state][symbol]
        current_state = next_state
    return current_state in dfa.dfa_accept  # Проверяем, находимся ли в терминальном состоянии


# Пример использования:
input_string = "a"
result = check_string(converter, input_string)
if result:
    print("Строка принята.")
else:
    print("Строка не принята.")