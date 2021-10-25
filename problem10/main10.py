"""
PROBLEM 10
language: python3.7
framework: atom
platform: mac

to run program:
    pass input_file_name, output_file_name, and number of strings in:
        helpers10.write_prob10_solution() on line 29
        eg.helpers10.write_prob10_solution("input.in", "output.out", 100)
    run this file
    output will be written in output_file_name

what this program does:
    Given the probabilistic context free grammar from input_file_name an
        integer n, the program outputs n strings generated in
        output_file_name. n is 1000 by default

testing: see tester10.py

file requirements:
    file contains valid PCNF with first line S:...
    nonterminals are in forms "A", "B", "C", ..., "Z"
    terminals are in forms "a", "b", "c", ..2., "z", "$"
    for each nonterminal V, the probabilities of its derived objects add up
        to 1. Probabilities are in (0, 1)
"""
import helpers10
helpers10.write_prob10_solution("input.in", "output.out")
