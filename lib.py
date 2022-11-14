#!/usr/bin/env python3
# Libraries
import csv

# Constants
EPSILON = '~'

class NFA:
    ''' place to store parts of the NFA '''
    def __init__(self):
        self.name = ""
        # formal definition of NFA
        self.states = {}
        self.alphabet = set()
        self.final_states = set()
        self.start_state = None
        self.delta = []
        # DFA stuff
        self.new_start_state = None
        self.new_states = set()
        self.new_final_states = set()
        self.new_delta = []
        # other stuff
        self.Er = {}
        self.alphabet_k = {}
        self.map = {}
        # trace -- data structures
        self.trace_delta = {}

    def print_NFA(self):
        ''' method to print the NFA stats '''
        print(f'Name:           {self.name}')
        print(f'States:         {self.states}')
        print(f'Alphabet:       {self.alphabet}')
        print(f'Final States:   {self.final_states}')
        print(f'Start State:    {self.start_state}')
        print(f'Delta:          {self.delta}')
        print('-------------------------------------------')
        print(f'DFA({self.name})= {self.delta}')
        print(f'StartStateDFA   = {self.new_start_state}')
        print(f'FinalStatesDFA  = {self.new_final_states}')
        print(f'NEW Delta       = {self.new_delta}')
        print(f'NEW States      = {self.new_states}')
        

    def get_NFA(self, _file):
        ''' get stuff from NFA file '''
        with open(_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            counter = 0
            for line in csv_reader:
                # first line -- NAME of NFA
                if counter == 0:
                    self.name += line[0]
                # second line -- list of states
                elif counter == 1:
                    for state in line:
                        if state:
                            if state[0] == '*':
                                self.states[state.replace('*', '')] = int(state[2:])
                            else:
                                self.states[state.replace('*', '')] = int(state[1:])
                # third line -- alphabet
                elif counter == 2:
                    k = 0
                    for char in line:
                        if char:
                            self.alphabet.add(char)
                            self.alphabet_k[char] = k
                            self.map[k] = char
                            k += 1

                # fourth line -- start state
                elif counter == 3:
                    self.start_state = line[0].replace('*', '')
                # fifth line -- set of final states
                elif counter == 4:
                    for final_state in line:
                        if final_state:
                            self.final_states.add(final_state.replace('*', ''))
                # the rest is the transition function
                else:
                    if line[0]:
                        self.delta.append((line[0].replace('*', ''), line[1], line[2].replace('*', '')))
                
                counter += 1
    
    def stringify(self, state_set):
        ''' method to change a set of states into a string that is uniform '''
        s = list(state_set)
        s = [state.replace('*', '') for state in s]
        
        s = sorted(s, key=lambda x: int(x[1:]))
        return " ".join(s)
            
    def compute_Er(self):
        ''' compute E(r) for the NFA '''
        # add start state to New Start State
        self.Er[self.start_state] = {self.start_state}
        # search through transition function to check epsilon transitions
        for transition in self.delta:
            # if there is an epsilon transition add the transition to the E(r) dict
            if transition[1] == EPSILON:
                if transition[0] in self.Er:
                    self.Er[transition[0]].add(transition[2])
                else:
                    self.Er[transition[0]] = {transition[2]}

        '''                                            ε      ε
        think about a transtion like this ->    (  q1 --> q2 --> q3  )
        this first for loop will only get:
        E(r) = {
            q1 : q2
            q2 : q3
        }  but we want q1 to have transitions from q1 : {q2, q3}
        so this next part will search through the sets of the keys in the dict and add the E[q2] to E[q1] because q2 is contained in E[q1] 
        '''
        # for key in dict
        for key in self.Er.keys():
            # make list of elements to check EPSILON transitions from
            check = list(self.Er[key])
            # while there is an element in check, search
            while check:
                if check[0] in self.Er:
                    for ele in self.Er[check[0]]:
                        if ele not in check:
                            check.append(ele)
                    self.Er[key] = self.Er[key].union(self.Er[check[0]])
                    check.pop(0)
                else:
                    check.pop(0)
        
        # make new start state an ordered string
        self.new_start_state = self.Er[self.start_state]
        # add starting state to new set of states
        self.new_states.add(self.stringify(self.new_start_state))
        
    def determine_new_states(self):
        ''' figuring out the new delta function and new set of states '''
        # initialize stack and list of sets
        stack = []
        sets = [set() for i in range(len(self.alphabet_k))]

        # for state in the new start state, check its transitions, add the transition states to set with corresponding alphabet transition
        # I.E. if the transtion is (q1, 0, q3) add q3 to the set sets[albhabet_k['0']]
        for state in self.new_start_state:
            for transition in self.delta:
                if state == transition[0] and transition[1] in self.alphabet_k:
                    index = self.alphabet_k[transition[1]]
                    sets[index].add(transition[2])

        # check each set and add stringified version to stack if not in stack
        for s in sets:
            if s and self.stringify(s) not in stack:
                stack.append(self.stringify(s))
    
        # loop while stack !empty
        while stack:
            # clear sets each loop reset
            for s in sets:
                s.clear()
            # if state is not already in set of new states add it
            if stack[0] not in self.new_states or stack[0] == self.stringify(self.new_start_state):
                self.new_states.add(stack[0])
                # loop through new state and check where is goes each letter in alphabet
                for state in stack[0].split(" "):
                    # if state in E(r), check transitions
                    if state in self.Er:
                        check = self.Er[state]
                        check.add(state)
                        # loop through transitions and add transition to corresponding set
                        # i.e. (q1, 'a', q3) ----> sets[self.alphabet_k[transition['a']]].add(q3)
                        for transition in self.delta:
                            if transition[0] in check and transition[1] in self.alphabet_k:
                                index = self.alphabet_k[transition[1]]
                                sets[index].add(transition[2])
                    else:
                        for transition in self.delta:
                            if state == transition[0] and transition[1] in self.alphabet_k:
                                index = self.alphabet_k[transition[1]]
                                sets[index].add(transition[2])
                # check each set
                for i in range(len(sets)):
                    if sets[i]:
                        # append to delta transition if set !empty
                        self.new_delta.append((stack[0], self.map[i], self.stringify(sets[i])))
                        if self.stringify(sets[i]) not in stack:
                            stack.append(self.stringify(sets[i]))
                    else:
                        self.new_delta.append((stack[0], self.map[i], None))
                # pop the element that we are checking
                stack.pop(0)
            else:
                # pop if stack[0] already in set of new states
                stack.pop(0)

    def determine_new_final_states(self):
        ''' find new final states '''
        for state in self.new_states:
            for final_state in self.final_states:
                if final_state in state.split(" "):
                    self.new_final_states.add(state)
    
    def create_trace_delta(self):
        ''' create data structure for trace -- dict of dicts '''
        self.trace_delta = {x:{} for x in self.states}
        # for transition in delta
        for d in self.delta:
            # if alphabet letter not in current state's dict, then add it and set value as destination state
            # i.e. (q1, a, q2) === {q1: {a:[q2]}}
            if d[1] in self.trace_delta[d[0]]:
                self.trace_delta[d[0]][d[1]].append(d[2])
            else:
                self.trace_delta[d[0]][d[1]] = [d[2]]

    def trace(self, string):
        ''' trace the NFA tree '''
        paths = []
        stack = []

        stack.append([self.start_state, string, [self.start_state]])

        while stack:
            popped = stack.pop()
            src = popped[0]
            # string
            s = popped[1]
            # list
            path = popped[2]
            
            # if the string is empty, we reached the end of the string
            if len(s) == 0:
                paths.append(path)

                if EPSILON in self.trace_delta[src] and len(path) == 1 and path[0] == src:
                    # if there is an epsilon transition from a given state, then for each destination, append that to the paths list to keep track of possible directions to take
                    for i in range(len(self.trace_delta[src][EPSILON])):
                        paths.append([self.trace_delta[src][EPSILON][i]])
                continue

            if s[0] in self.trace_delta[src]:
                for i in range(len(self.trace_delta[src][s[0]])):
                    stack.append([self.trace_delta[src][s[0]][i], s[1:], path + [self.trace_delta[src][s[0]][i]]])

                    child = self.trace_delta[src][s[0]][i]

                    if EPSILON in self.trace_delta[child]:
                        for i in range(len(self.trace_delta[child][EPSILON])):
                            stack.append([self.trace_delta[child][EPSILON][i], s[1:], path + [self.trace_delta[child][EPSILON][i]]])
                
            if EPSILON in self.trace_delta[src] and len(path) == 1 and path[0] == self.start_state and src == self.start_state:
                for i in range(len(self.trace_delta[src][EPSILON])):
                    stack.append([self.trace_delta[src][EPSILON][i], s, [self.trace_delta[src][EPSILON][i]]])

        return paths
    
    def trace_final_states(self, paths):
        result = filter(lambda x: x[-1] in self.final_states, paths)
        return list(result)

    def print_trace_to_file(self, paths, final_paths):
        with open("output_trace.csv", "w") as f:
            f.write(f'This is the file that contains the NFA trace for {self.name}.\n')
            f.write(f'This will be an example of trace_DarkLamp program which traces an NFA and shows possible paths for the NFA given a string.\n')
            f.write(f'by Ryan McCann and Matt Kennedy\n\n')
            f.write(f'NFA:\nStates: {self.states}\nSigma: {self.alphabet}\nStart State: {self.start_state}\nFinal States: \n')
            for fs in self.final_states:
                f.write(f'{fs}\n')
            f.write(f'DELTA: \n')
            for d in self.delta:
                f.write(f'{d}\n')
            f.write('\n')
            f.write("All possible paths below:\n")
            for path in paths:
                f.write(f'{path}\n')
            f.write('\n')
            f.write("These are all paths that make it to a final state:\n")
            for path in final_paths:
                f.write(f'{path}\n')
            f.write('\n\n')
            f.write(f'The number of leaves on tree was {len(paths)}.\n')
            f.write(f'The number of leaves in final state was {len(final_paths)}')
            

    def print_DFA_to_file(self):
        ''' print the new DFA to a csv file '''
        with open('output_nfa2dfa.csv', 'w') as f:
            f.write(f'This is the file that contains the NFA to DFA for {self.name}.\n')
            f.write(f'This will be an example of nfa2dfa_DarkLamp program which transforms a given NFA to an equivalent DFA.\n')
            f.write(f'The output will be in similar format to the input of NFA below, and states are comma separated.\nNOTE: some states look like this: q1 q2, this is one state, the space is a part of the state.\n')
            f.write(f'by Ryan McCann and Matt Kennedy\n\n')
            f.write(f'NFA:\nStates: {self.states}\nSigma: {self.alphabet}\nStart State: {self.start_state}\nFinal States: \n')
            for fs in self.final_states:
                f.write(f'{fs}\n')
            f.write(f'DELTA: \n')
            for d in self.delta:
                f.write(f'{d}\n')
            f.write('\n')
            
            f.write(f'The DFA from NFA({self.name})\n')
            w = csv.writer(f)
            w.writerow([self.name])
            w.writerow(list(self.new_states))
            w.writerow(list(self.alphabet))
            w.writerow([self.stringify(self.new_start_state)])
            w.writerow(list(self.new_final_states))
            for transition in self.new_delta:
                w.writerow(transition)
