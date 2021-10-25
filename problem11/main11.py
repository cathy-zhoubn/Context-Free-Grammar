"""
PROBLEM 11
language: python3.7
framework: atom
platform: mac

to run program:
    pass input_file_name, output_file_name, and string_for_derivation in:
        helpers11.write_prob11_solution() on line 29
        eg.helpers11.write_prob11_solution("input.in", "output.out", "babaab")
    run this file
    output will be written in output_file_name

what this program does:
    given the probabilistic context free grammar from input_file_name and a
        string, the program outputs all possible derivations of the string and
        their respective proabilities.

testing: see tester11.py

file requirements:
    file contains valid PCNF with first line S:...
    nonterminals are in forms "A", "B", "C", ..., "Z"
    terminals are in forms "a", "b", "c", ..2., "z", "$"
    for each nonterminal V, the probabilities of its derived objects add up
        to 1. Probabilities are in (0, 1)
"""
import helpers11
helpers11.write_prob11_solution("input.in", "output.out", "aab")
