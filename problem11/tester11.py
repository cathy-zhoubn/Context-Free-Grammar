"""
PROBLEM 11
language: python3.7
framework: atom
platform: mac

test data in folder:
    test1.in:
        this file contains the original context-free grammar in problem 11. the
        strings required in the problem ("aab", "abab", "abb") are checked, as
        as well as others such as: "aaa","bbb", "aba", "bababbbabab", "abbab",
        "aaaaab". output is put into test1.out

    test2.in:
        this file contains an unambiguous context-free grammar. various strings
        are used for checking. output is put into test2.out
"""

import helpers11


def check11(input_file, output_file, str_list):
    pcnf = helpers11.read_PCNF(input_file)
    fw = open(output_file, "w")
    derivation_list = []
    for string in str_list:
        derivation_list.append(pcnf.get_derivations(string))
    for i in range(len(derivation_list)):
        fw.write("Derivations for string \"" + str_list[i] + "\" are:\n")
        if derivation_list[i] is None:
            fw.write("Not in the language\n")
        else:
            for derivation in derivation_list[i]:
                fw.write(str(derivation))
        fw.write("\n")
    fw.write("\r\n")
    fw.close()


check11("test1.in", "test1.out", ["aab", "abab", "abb", "aaa",
                                  "bbb", "aba", "bababbbabab", "abbab", "aaaaab"])
check11("test2.in", "test2.out", ["a", "b", "c", "aa", "bb", "abb", "aab", "aba", "aabb", "bbaa"])

print("checked!")
