"""
PROBLEM 7
language: python3.7
framework: atom
platform: mac

to run program:
    pass input_file_name, output_file_name, and number of strings in:
        helpers7.write_prob7_solution() on line 27
        eg.helpers7.write_prob7_solution("input.in", "output.out", 100)
    run this file
    output will be written in output_file_name

what this program does:
    given the context free grammar from input_file_name an integer n, the
        program outputs the first n strings in the short-lex order in
        output_file_name. n is 1000 by default

testing: see tester7.py

file requirements:
    file contains valid CFG with first line S:...
    nonterminals are in forms "A", "B", "C", ..., "Z"
    terminals are in forms and in order "$", "a", "b", "c", ..., "z",
"""
import helpers7
helpers7.write_prob7_solution("test1.in", "test1.out")
