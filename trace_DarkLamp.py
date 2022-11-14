#!/usr/bin/env python3

# Team Name = DarkLamp
# Team Member = Ryan McCann
# Theory of Computing Project #2, fa22
# nfa 2 dfa program

from lib import NFA

def main():
    ''' to trace an NFA '''
    # trace_DarkLamp
    nfa = NFA()
    nfa.get_NFA("N6.csv")
    nfa.create_trace_delta()
    print(nfa.trace_delta)
    # input random string into nfa.trace
    paths = nfa.trace('10101')
    result = nfa.trace_final_states(paths)
    nfa.print_trace_to_file(paths, result)

if __name__ == "__main__":
    main()