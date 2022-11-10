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

    def print_NFA(self):
        ''' method to print the NFA stats '''
        print(f'Name:           {self.name}')
        print(f'States:         {self.states}')
        print(f'Alphabet:       {self.alphabet}')
        print(f'Final States:   {self.final_states}')
        print(f'Start State:    {self.start_state}')
        print(f'Delta:          {self.delta}')
        print(f'E(r) =          {self.Er}')
        print(f'StartStateDFA = {self.new_start_state}')

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
                                self.states[state] = int(state[2:])
                            else:
                                self.states[state] = int(state[1:])
                # third line -- alphabet
                elif counter == 2:
                    for char in line:
                        if char:
                            self.alphabet.add(char)
                # fourth line -- start state
                elif counter == 3:
                    self.start_state = line[0]
                # fifth line -- set of final states
                elif counter == 4:
                    for final_state in line:
                        if final_state:
                            self.final_states.add(final_state)
                # the rest is the transition function
                else:
                    self.delta.append((line[0], line[1], line[2]))
                
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
            print(transition)
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
        # print(f'E(r) original {self.Er}')
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
        
        print(f'\nE(r) = {self.Er}')
        # make new start state an ordered string
        self.new_start_state = self.Er[self.start_state]
        
    def determine_new_states(self):
        ''' figuring out the new delta function and new set of states '''
        # add starting state to new set of states
        self.new_states.add(self.stringify(self.new_start_state))
        print(f'new states ----> {self.new_states}')

        stack = []
        set0, set1 = set(), set()
        for state in self.new_start_state:
            set0.clear()
            set1.clear()
            for transition in self.delta:
                if state == transition[0]:
                    if transition[1] == '0':
                        set0.add(transition[2])
                    else:
                        set1.add(transition[2])
            if set0:
                stack.append(self.stringify(set0))
            if set1:
                stack.append(self.stringify(set1))

        print(f'initial stack --- > {stack}\n')
        set0.clear()
        set1.clear()
        k = -1
        while stack:
            k +=1
            set0.clear()
            set1.clear()
            print(stack[0])
            # if state is not already in set of new states add it
            if stack[0] not in self.new_states or stack[0] == self.stringify(self.new_start_state):
                self.new_states.add(stack[0])
                # loop through new state and check where is goes with 0 and 1 ---> TODO account for epsilon transitions
                for state in stack[0].split(" "):
                    # if state in E(r) check where 0 or 1 goes for each element in that set
                    if state in self.Er:
                        check = self.Er[state]
                        check.add(state)
                        print(f'{k}.  check = {check}')
                        for transition in self.delta:
                            if transition[0] in check:
                                if transition[1] == '0':
                                    set0.add(transition[2])
                                elif transition[1] == '1':
                                    set1.add(transition[2])
                                else:
                                    pass
                    else:
                        for transition in self.delta:
                            if state == transition[0]:
                                if transition[1] =='0':
                                    set0.add(transition[2])
                                elif transition[1] == '1':
                                    set1.add(transition[2])
                                else:
                                    pass
                    print(f'** set1 = {set1}')
                
                
                if set0:
                    self.new_delta.append((stack[0], '0', self.stringify(set0)))
                    if self.stringify(set0) not in stack:
                        stack.append(self.stringify(set0))
                        print(f'>>> {self.stringify(set1)} as 0')
                else:
                    self.new_delta.append((stack[0], '0', None))
                if set1:
                    self.new_delta.append((stack[0], '1', self.stringify(set1)))
                    if self.stringify(set1) not in stack:
                        stack.append(self.stringify(set1))
                        print(f'>>> {self.stringify(set1)} as 1')
                else:
                    self.new_delta.append((stack[0], '1', None))
                stack.pop(0)
            else:
                stack.pop(0)
                print("end\n")

        print(self.new_states)
        print(self.new_delta)

    def determine_new_final_states(self):
        for state in self.new_states:
            for final_state in self.final_states:
                if final_state in state.split(" "):
                    self.new_final_states.add(state)
        print(self.new_final_states)

    def print_DFA_to_file(self):
        with open('output.csv', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(list(self.name))
            csv_writer.writerow(list(self.new_states))
            csv_writer.writerow(list(self.alphabet))
            csv_writer.writerow(list(self.new_start_state))
            csv_writer.writerow(list(self.new_final_states))
            for transition in self.new_delta:
                csv_writer.writerow(transition)



        


n = NFA()
n.get_NFA("N1.csv")
n.compute_Er()
# n.print_NFA()
n.determine_new_states()
n.determine_new_final_states()
n.print_DFA_to_file()

