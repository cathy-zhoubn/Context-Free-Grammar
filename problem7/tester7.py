"""
PROBLEM 7
language: python3.7
framework: atom
platform: mac

test data in folder:
    test1.in:
        this file contains the original langauge in the problem. the language
            of this grammar is any string containing "a" and "b" that
            starts with "a", such as "abababababbabbabbaba".
            test strings and result are put into the file, test1.out.

    test2.in:
        this file contains a grammar with null nonterminal and null in its
            language. the language should be a i number of "a"s followed by j
            number of "b"s, where i>=j.

    test3.in:
        the language of this language should be all strings with "a" and "b"
            that has the first and last character the same
"""

import helpers7

helpers7.write_prob7_solution("test1.in", "test1.out")
helpers7.write_prob7_solution("test2.in", "test2.out")
helpers7.write_prob7_solution("test3.in", "test3.out")
print("checked!")
