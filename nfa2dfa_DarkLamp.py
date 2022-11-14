#!/usr/bin/env python3

# Team Name = DarkLamp
# Team Member = Ryan McCann
# Theory of Computing Project #2, fa22
# trace program

from lib import NFA

def main():
    ''' to get equivalent DFA from NFA '''
    # nfa2dfa_DarkLamp
    nfa = NFA()
    nfa.get_NFA("N6.csv")
    nfa.compute_Er()
    nfa.determine_new_states()
    nfa.determine_new_final_states()
    # prints information regarding the NFA and its DFA
    nfa.print_NFA()
    nfa.print_DFA_to_file()

if __name__ == "__main__":
    main()