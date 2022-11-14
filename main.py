#!/usr/bin/env python3

# Team Name = DarkLamp
# Team Member = Ryan McCann
# Theory of Computing Project #2, fa22

from nfa2dfa_DarkLamp import NFA

def main():
    ''' to get equivalent DFA from NFA '''
    # nfa2dfa_DarkLamp
    nfa = NFA()
    nfa.get_NFA("N5.csv")
    nfa.compute_Er()
    nfa.determine_new_states()
    nfa.determine_new_final_states()
    # prints information regarding the NFA and its DFA
    nfa.print_NFA()
    nfa.print_DFA_to_file()

    ''' to trace an NFA '''
    # trace_DarkLamp
    nfa.create_trace_delta()
    print(nfa.trace_delta)
    # input random string into nfa.trace
    paths = nfa.trace('10101')
    result = nfa.trace_final_states(paths)
    nfa.print_trace_to_file(paths, result)

if __name__ == "__main__":
    main()