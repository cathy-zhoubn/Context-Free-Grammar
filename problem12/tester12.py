"""
PROBLEM 12
language: python3.7
framework: atom
platform: mac

test data in folder:
    grammar.in and strings.in:
        these file contain the original context-free grammar and strings in
        problem 12. estimation is put into output.out

    test1_grammar.in and test1_strings.in:
        the grammar is adapted and the strings are obtained from the
        probabilistic context free grammar in test1_original.txt. this grammar
        is not ambiguous. estimation is put into test1.out

    test2_grammar.in and test2_strings.in:
        this grammar is amiguous. the original grammar is stored in
            test2_original.txt and the output is put into test2.out

    from these testing, we can observe that the algorithm is accurate.
"""

import helpers12


helpers12.write_prob12_solution("grammar.in", "strings.in", "output.out")
helpers12.write_prob12_solution("test1_grammar.in", "test1_strings.in", "test1.out")
helpers12.write_prob12_solution("test2_grammar.in", "test2_strings.in", "test2.out")


print("checked!")
