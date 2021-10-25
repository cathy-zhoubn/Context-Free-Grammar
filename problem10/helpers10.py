"""
PROBLEM 10, helpers
language: python3.7
framework: atom
platform: mac
this file contain all functions
"""
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


class PRule(Rule):
    """
    this class is a class for one rule in PCFG
    """

    def __init__(self, left, right, prob):
        """
        @param prob is the probability in [0,1)
        """
        super().__init__(left, right)
        self.prob = prob

    def getProb(self):
        return self.prob

    def __str__(self):
        output = self.left + ":"
        for element in self.right:
            output += str(element)
        output += " " + str(self.prob)
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


class PCFG(CFG):
    """
    class of probabilistic context free grammar
    """

    def __init__(self, rules):
        """
        rules is a set of PRules
        """
        super().__init__(rules)

    def get_prob_list(self, nonterm):
        """
        for a nonterminal, this function gets the list that it can be derived
        into. Each element in the list is a tuple, (derived, probability).
        Probability adds up. eg. If S -> a 0.3|b 0.3 |c 0.4, it returns
        [(a, 0.3), (b, 0.6), (c, 1.0)]
        """
        output = []
        total_prob = 0
        for rule in self.rules:
            if rule.getLeft() == nonterm:
                total_prob += rule.getProb()
                output.append((rule.getRight(), total_prob))
        return output

    def get_rand_string(self):
        """
        get a string in the pcfg following the probability.
        """
        def find_substitute(prob_list):
            """
            decide the substitute given the probability list
            """
            rand = random.random()
            if rand < prob_list[0][1]:
                return prob_list[0][0]
            for j in range(len(prob_list)-1):
                if rand < prob_list[j+1][1] and rand >= prob_list[j][1]:
                    return prob_list[j+1][0]

        string = [self.start]
        i = 0
        while i < len(string):
            char = string[i]
            if is_terminal(char):
                i += 1
            else:
                prob_list = self.get_prob_list(char)
                substitute = find_substitute(prob_list)
                string = replace(string, char, substitute)
        to_str = ""
        for char in string:
            if char != "$":
                to_str += char
        if to_str == "":
            to_str = "$"
        return to_str


def read_PCFG(file_name):
    """
    reads from a file with name @param file_name and instantiate rules and PCFG
    for each line in the file.
    """
    fo = open(file_name, "r")
    fo_list = fo.read().splitlines()
    rules = []
    for line in fo_list:
        rule = line.split(" ")[0]
        prob = float(line.split(" ")[1])
        left = rule.split(":")[0]
        right = []
        for char in rule.split(":")[1]:
            right.append(char)
        rules.append(PRule(left, right, prob))
    fo.close()
    return PCFG(rules)


def write_prob10_solution(input_file_name, output_file_name, n=1000):
    pcfg = read_PCFG(input_file_name)
    fw = open(output_file_name, "w")
    lines = int(n/10)
    last_line = n % 10
    for line in range(lines):
        output = ""
        for i in range(10):
            output += pcfg.get_rand_string() + " "
        output = output[:-1]
        output += "\n"
        fw.write(output)
    output = ""
    for i in range(last_line):
        output += str(pcfg.get_rand_string()) + " "
        output = output[:-1]
    output += "\r\n"
    fw.write(output)
    fw.close()
