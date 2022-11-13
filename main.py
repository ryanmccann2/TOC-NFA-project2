#!/usr/bin/env python3
from nfa2dfa_DarkLamp import NFA

def main():
    nfa = NFA()
    nfa.get_NFA("N1.csv")
    nfa.compute_Er()
    nfa.determine_new_states()
    nfa.determine_new_final_states()
    nfa.print_NFA()
    nfa.print_DFA_to_file()

if __name__ == "__main__":
    main()