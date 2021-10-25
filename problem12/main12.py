"""
PROBLEM 12
language: python3.7
framework: atom
platform: mac

to run program:
    pass input_file_name, output_file_name, and string_for_derivation in:
        helpers11.write_prob11_solution() on line 18
        eg.helpers11.write_prob11_solution("input.in", "output.out", "babaab")
    run this file
    output will be written in output_file_name

what this program does:
    given the probabilistic context free grammar without probabilities from
        input_file_name and strings generated from the grammar, the program
        outputs full pcfg with estimated probability of each rule.

testing and accuracy analysis: see tester12.py
    accuracy could be adjusted in helpers12.py on line 347, the DEVIATION
        parameter. this is the parameter that controls what is considered as a
        "local optimum", so the smaller it is, the more iterations of update
        the algorithm performs.

file requirements:
    file contains valid CNG with first line S:...
    nonterminals are in forms "A", "B", "C", ..., "Z"
    terminals are in forms "a", "b", "c", ..., "z", "$"

sources used:
    http://karlstratos.com/notes/em_inside_outside_formulation.pdf
"""
import helpers12
helpers12.write_prob12_solution("grammar.in", "strings.in", "output.out")
