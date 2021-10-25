"""
PROBLEM 6, helpers
language: python3.7
framework: atom
platform: mac
this file contain all functions
"""
import copy
import random


def is_terminal(char):
    """
    function checks if a length 1 string is a terminals
    it is terminal if it is lower case character of is "$"
    """
    if len(char) == 1:
        return ((ord(char) > 96) and (ord(char) < 123)) or ord(char) == 36
    else:
        return False


def replace(string, nonterm, substitute):
    index = string.index(nonterm)
    return string[:index] + substitute + string[index+1:]


class Rule:
    """
    this class is a class for one rule in context free grammar
    """

    def __init__(self, left, right):
        """
        a rule consists of one nonterminal str, @param left
        it is derived into a list of nonterminals and terminals, @param right
            the right side is represented as list because later algorithms will
            add nonterminals in form "V0" and "U0".
        """
        self.left = left
        self.right = right

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def __str__(self):
        output = self.left + ":"
        for element in self.right:
            output += str(element)
        return output


class CFG:
    """
    the class of context free grammar
    """

    def __init__(self, rules):
        """
        initialization takes a set of rules, rules are in the class Rule
        parameters of the class include terminals, and nonterminals.
        """
        self.rules = rules
        self.terminals = set()
        for rule in self.rules:
            for character in rule.getRight():
                if is_terminal(character) and character not in self.terminals:
                    self.terminals.add(character)
        self.update_nonterminals()  # initiates nonterminals
        self.update_start()

    def update_nonterminals(self):
        """
        set the list of nonterminals as all nonterminals on the left
        """
        self.nonterminals = set()
        for rule in self.rules:
            if rule.getLeft() not in self.nonterminals:
                self.nonterminals.add(rule.getLeft())

    def update_start(self):
        if "S0" in self.nonterminals:
            self.start = "S0"
        else:
            self.start = "S"

    def get_rules(self):
        return self.rules

    def get_nonterminals(self):
        return self.nonterminals

    def get_terminals(self):
        return self.terminals

    def get_start(self):
        return self.start

    def __str__(self):
        output = []
        for rule in self.rules:
            output.append(str(rule))
        return str(output)

    def cfg_to_cnf(self):
        """
        converts a cfg to cnf form
        """

        def start(self):
            """
            adds a rule "S0:S" to the rules
            """
            if self.start == "S":
                self.rules.add(Rule("S0", ["S"]))

        def replace_terminals(self):
            """
            replaces all terminals in non-unit rule with a nonterminal and
            adds a rule that the nonterminal equals the terminal
            """
            new_nonterm_count = 0
            self.rules = list(self.rules)
            for rule in self.rules:
                right = rule.getRight()
                if len(right) > 1:
                    for character in right:
                        if is_terminal(character):
                            new_nonterm = "V" + str(new_nonterm_count)
                            self.rules.append(Rule(new_nonterm, [character]))
                            rule.right = replace(right, character, [new_nonterm])
                            new_nonterm_count += 1
            self.rules = set(self.rules)

        def split_rules(self):
            """
            splits a rule that is longer than 2 to rules of length 2
            """
            self.rules = list(self.rules)
            new_nonterminal_count = 0
            for rule in self.rules:
                right = rule.getRight()
                while(len(right) > 2):
                    new_nonterminal = "U" + str(new_nonterminal_count)
                    new_nonterminal_count += 1
                    self.rules.append(Rule(new_nonterminal, right[0:2]))
                    rule.right = [new_nonterminal] + right[2:]
                    right = rule.getRight()
            self.rules = set(self.rules)

        def remove_unit(self):
            """
            remove unit rules such as A:B
            """
            self.rules = list(self.rules)
            i = 0
            while i in range(len(self.rules)):
                rule = self.rules[i]
                right = rule.getRight()
                if len(right) == 1 and (not is_terminal(right[0])):
                    left = rule.getLeft()
                    for other_rule in self.rules:
                        if other_rule.getLeft() == right[0]:
                            self.rules.append(Rule(left, other_rule.getRight()))
                    self.rules.remove(rule)
                else:
                    i += 1
            self.rules = set(self.rules)

        def remove_null(self):
            """
            remove null rules such as A:$
            ***This version of remove_null assumes that $ is a part of the
                nonterminal.
            """
            self.rules = list(self.rules)
            null_nonterminals = []
            for rule in self.rules:
                while ("$" in rule.getRight()) and (len(rule.getRight()) > 1):
                    rule.getRight().remove("$")
                if (rule.getRight() == ["$"] and rule.getLeft() != "S0"):
                    null_nonterminals.append(rule.getLeft())
                    self.rules.remove(rule)

            for rule in self.rules:
                for character in rule.getRight():
                    if character in null_nonterminals:
                        new = replace(rule.getRight(), character, [])
                        if len(new) > 0:
                            self.rules.append(Rule(rule.getLeft(), new))
            self.rules = set(self.rules)

        def remove_duplicates(self):
            self.rules = list(self.rules)
            i = 0
            while i < len(self.rules):
                j = i+1
                while j < len(self.rules):
                    rule1 = self.rules[i]
                    rule2 = self.rules[j]
                    if rule1.getLeft() == rule2.getLeft() and rule1.getRight() == rule2.getRight():
                        self.rules.remove(rule2)
                    else:
                        j += 1
                i += 1
            self.rules = set(self.rules)

        start(self)
        split_rules(self)
        replace_terminals(self)
        remove_unit(self)  # this extra remove_unit step is for setting up for remove_null
        remove_null(self)
        remove_unit(self)
        remove_duplicates(self)
        self.update_nonterminals()
        self.update_start()


class CNF(CFG):
    """
    the class of CNF
    """

    def __init__(self, cfg):
        """
        initialization takes in @param cfg of class CFG
        initializes self.rules, nonterminals, and terminals respectively
        """
        cfg.cfg_to_cnf()
        self.rules = cfg.get_rules()
        self.nonterminals = cfg.get_nonterminals()
        self.terminals = cfg.get_terminals()
        self.start = cfg.get_start()

    def has(self, string):
        """
        uses the cyk algorithm to see if the string is in the language
        """
        str_len = len(string)
        array = []
        for i in range(str_len):  # initializes the array
            array.append([])
            for j in range(str_len):
                array[i].append(set())

        for i in range(str_len):  # calculate the fist row of the array
            for rule in self.rules:
                right = copy.copy(rule.getRight())
                if(right[0] == string[i] and len(right) == 1):
                    array[0][i].add(rule.getLeft())

        for length in range(1, str_len):  # performs update
            for span in range(str_len-length):
                for partition in range(length):
                    for rule in self.rules:
                        right = rule.getRight()
                        if(len(right) == 2):
                            if (right[0] in array[partition][span]) and (right[1] in array[length-partition-1][span + partition+1]):
                                array[length][span].add(rule.getLeft())
        return self.start in array[str_len-1][0]


def read_CFG(file_name):
    """
    reads from a file with name @param file_name and instantiate rules and CFG
    for each line in the file.
    """
    fo = open(file_name, "r")
    fo_list = fo.read().splitlines()
    rules = set()
    for line in fo_list:
        left = line.split(":")[0]
        right = []
        for char in line.split(":")[1]:
            right.append(char)
        rules.add(Rule(left, right))
    fo.close()
    return CFG(rules)


def write_prob6_solution(input_file_name, output_file_name, string_to_check):
    """
    chech @param string and write the solution with cfg inputted from @param
    input_file_name
    """
    cfg = read_CFG(input_file_name)  # input file name here
    cnf = CNF(cfg)
    fw = open(output_file_name, "w+")
    fw.write(str(cnf.has(string_to_check)))  # input string here
    fw.close()
