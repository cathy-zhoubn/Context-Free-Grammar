"""
PROBLEM 10
language: python3.7
framework: atom
platform: mac

test data in folder:
    test1.in:
        this file contains the original context-free grammar in problem 10. The
            language of this grammar is any string containing "a" and "b", with
            the probability that the first character is "a" 0.7 and "b" 0.3
        test strings and result are put into the file, test1.out.

    test2.in:
        this file contains a grammar with null nonterminal and null in its
            language. the language should be a i number of "a"s followed by j
            number of "b"s, where i>=j.

    test3.in:
        the language of this language should be all strings with "a" and "b"
            that has the first and last character the same. The probability
            that "a" happens is larger than "b".

    test4.in:
        The language of this grammar is any string containing "a" and "b" that
            starts with "a", such as "abababababbabbabbaba". the arobability
            that "a" happens is larger than "b".
"""

import helpers10

helpers10.write_prob10_solution("test1.in", "test1.out")
helpers10.write_prob10_solution("test2.in", "test2.out")
helpers10.write_prob10_solution("test3.in", "test3.out")
helpers10.write_prob10_solution("test4.in", "test4.out")
print("checked!")
