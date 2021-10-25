"""
PROBLEM 6
language: python3.7
framework: atom
platform: mac

to run program:
    input files and output files should be in the folder, problem6
    pass input_file_name, output_file_name, and string_to_check in:
        helpers6.write_prob6_solution() on line 32
        eg.helpers6.write_prob6_solution("input.in", "output.out", "babaab")
    run this file

what this program does:
    Given the context free grammar from input_file_name and a string from
        string_to_check, the program outputs whether the string is in the
        grammar.

file requirements:
    file contains valid CFG with start symbol as "S"
    nonterminals are in forms "A", "B", "C", ..., "Z"
    terminals are in forms "a", "b", "c", ..., "z", "$"

testing: see tester6.py

sources used:
    https://en.wikipedia.org/wiki/CYK_algorithm
    https://cs.nyu.edu/courses/fall07/V22.0453-001/cnf.pdf
"""

import helpers6
helpers6.write_prob6_solution("input.in", "input.out", "ababba")
