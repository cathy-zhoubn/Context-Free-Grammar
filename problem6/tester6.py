"""
PROBLEM 6
language: python3.7
framework: atom
platform: mac

test data in folder:
    test1.in:
        this file contains the original context-free grammar in problem 6. The
            language of this grammar is any string containing "a" and "b" that
            starts with "a", such as "abababababbabbabbaba".
        test strings and result are put into the file, test1.out.
            the write_prob6_solution was modified for format purposes.
        the output confirms this.

    test2.in:
        this file contains a grammar with null nonterminal and null in its
            language. the language should be a i number of "a"s followed by j
            number of "b"s, where i>=j.

    test3.in:
        the language of this language should be all strings with "a" and "b"
            that has the first and last character the same

"""

import helpers6
import random


def check_two_lists(true_list, false_list, input_file, output_file):
    cfg = helpers6.read_CFG(input_file)  # input file name here
    cnf = helpers6.CNF(cfg)
    fw = open(output_file, "w+")
    for string in true_list:
        fw.write("string " + string + " : " +
                 str(cnf.has(string)) + "\n")  # input string here
    fw.write("\n")
    for string in false_list:
        fw.write("string " + string + " : " +
                 str(cnf.has(string)) + "\n")  # input string here
    fw.close()


def check_test1():

    true_list = []
    for i in range(50):
        length = random.randint(0, 50)
        string = "a"
        for j in range(length):
            character = random.randint(0, 2)
            if character == 0:
                string += "a"
            if character == 1:
                string += "b"
        true_list.append(string)

    false_list = []
    for i in range(30):
        length = random.randint(0, 50)
        string = "b"
        for j in range(length):
            character = random.randint(0, 2)
            if character == 0:
                string += "a"
            else:
                string += "b"
        false_list.append(string)

    for i in range(20):
        length = random.randint(0, 50)
        string = "a"
        for j in range(length):
            character = random.randint(0, 2)
            if character == 0:
                string += "c"
            else:
                string += "d"
    check_two_lists(true_list, false_list, "test1.in", "test1.out")


def check_test2():
    true_list = ["$", "a", "aab", "ab", "aabb", "aaaa", "aaabbb", "aaaaaaab"]
    false_list = ["b", "abbb", "aaaabbbbbbbb", "abba", "abbabbababa", "bba", "aaaacbbb"]
    check_two_lists(true_list, false_list, "test2.in", "test2.out")


def check_test3():
    true_list = ["aa", "bb", "aaa", "bbb", "aba", "bab", "abababbaba", "bababbabab"]
    false_list = ["$", "a", "b", "ab", "ba", "abababab", "bababbaba", "cababababc"]
    check_two_lists(true_list, false_list, "test3.in", "test3.out")


check_test1()
check_test2()
check_test3()
print("checked!")
