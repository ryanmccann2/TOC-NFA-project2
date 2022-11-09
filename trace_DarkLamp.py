#!/usr/bin/env python3
import csv

class NFA:
    ''' place to store parts of the NFA '''
    def __init__(self):
        self.name = ""
        self.states = set()
        self.alphabet = set()
        self.final_states = set()
        self.start_state = None
        self.delta = []

    def print_NFA(self):
        print(f'Name: {self.name}')
        print(f'States: {self.states}')
        print(f'Alphabet: {self.alphabet}')
        print(f'Final States: {self.final_states}')
        print(f'Start State: {self.start_state}')
        print(f'Delta: {self.delta}')

    def get_NFA(self, _file):
        ''' get stuff from NFA file '''
        with open(_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            counter = 0
            for line in csv_reader:
                if counter == 0:
                    self.name += line[0]
                elif counter == 1:
                    for state in line:
                        if state:
                            self.states.add(state)
                elif counter == 2:
                    for char in line:
                        if char:
                            self.alphabet.add(char)
                elif counter == 3:
                    self.start_state = line[0]
                elif counter == 4:
                    for final_state in line:
                        if final_state:
                            self.final_states.add(final_state)
                else:
                    self.delta.append((line[0], line[1], line[2]))
                
                counter += 1

n = NFA()
n.get_NFA("N1.csv")
n.print_NFA()
