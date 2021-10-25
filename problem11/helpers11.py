"""
PROBLEM 11, helpers
language: python3.7
framework: atom
platform: mac
this file contain all functions
"""
import copy


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


class Character:
    """
    includes information of the character and what it is derived into.
    used in listing parsetrees in cyk
    """

    def __init__(self, rule, next1, next2=None):
        """
        @param the_character: the character that is initiated
        @param rule: the rule for derivation
        @param next1: Character for the 1st nonterminal in derivation or the
            terminal
        @param next2: Character for the 2nd nonterminal.
            If it is a terminal, next2 is None
        """
        self.rule = rule
        self.char = rule.getLeft()
        if next2 is None:
            self.terminates = True
            self.term = rule.getRight()[0]
        else:
            self.terminates = False
            self.nonterm1 = next1
            self.nonterm2 = next2

    def __str__(self):
        return self.char

    def is_terminated(self):
        return self.terminates

    def get_term(self):
        return self.term

    def get_nonterm1(self):
        return self.nonterm1

    def get_nonterm2(self):
        return self.nonterm2

    def prob(self):
        if self.terminates:
            return self.rule.getProb()
        else:
            return self.rule.getProb() * self.nonterm1.prob() * self.nonterm2.prob()


class Derivation:
    def __init__(self, start, derivation_list):
        """
        the class represents a leftmost derivation with probability
        @param start is the character of class Character that the derivation
            starts
        @param derivation_list is the list containing each step of derivation
        """
        self.probability = start.prob()
        self.derivation_list = derivation_list

    def __str__(self):
        output = ""
        for step in self.derivation_list:
            for character in step:
                output += character
            output += "->"
        output = output[:-2]
        output += " " + str(self.probability) + "\n"
        return output


class PCNF(PCFG):
    """
    the class of probabilistic CNF
    """

    def __init__(self, rules):
        """
        initialization takes in a list of rules or class PRule. Rules are
        assumed to be in probabilistic CNF.
        """
        super().__init__(rules)

    def parse(self, string):
        """
        uses the cyk algorithm to list all possible leftmost derivations of
        @param string and its probabilities. Output an array of the derivation
            table.
        """
        str_len = len(string)
        table = []
        for i in range(str_len):  # initializes the array
            table.append([])
            for j in range(str_len):
                table[i].append(set())

        for i in range(str_len):  # calculate the fist row of the array
            for rule in self.rules:
                right = rule.getRight()
                if(right[0] == string[i] and len(right) == 1):
                    table[0][i].add(Character(rule, right[0]))

        for length in range(1, str_len):  # performs update
            for span in range(str_len-length):
                for partition in range(length):
                    for rule in self.rules:
                        right = rule.getRight()
                        if(len(right) == 2):
                            nonterm1 = set()
                            nonterm2 = set()
                            for character in table[partition][span]:
                                if str(character) == right[0]:
                                    nonterm1.add(character)
                            for character in table[length-partition-1][span + partition+1]:
                                if str(character) == right[1]:
                                    nonterm2.add(character)
                            for char1 in nonterm1:
                                for char2 in nonterm2:
                                    table[length][span].add(Character(rule, char1, char2))
        return table

    def get_derivations(self, string):
        """
        method returns all derivations of the string and their probabilities
        output is a list of tuples (derivations, probability) arranged by
            probabilities.
        """
        def derive(character, derivation_list):
            """
            make a derivation step given the previous derivations in @param
                derivation_list and @param character of class character
            @param derivation_list is a list with each item being the list representing
                the string obtained in a step
            """
            last_step = copy.copy(derivation_list[-1])
            if character.is_terminated():
                new = replace(last_step, str(character), [character.get_term()])
                derivation_list.append(new)
            else:
                nonterm1 = character.get_nonterm1()
                nonterm2 = character.get_nonterm2()
                new = replace(last_step, str(character), [str(nonterm1), str(nonterm2)])
                derivation_list.append(new)
                derive(nonterm1, derivation_list)
                derive(nonterm2, derivation_list)
            return derivation_list

        table = self.parse(string)
        list_for_start = set()
        reacheable = False
        for character in table[-1][0]:
            if str(character) == self.start:
                reacheable = True
                list_for_start.add(character)
        if not reacheable:
            return None
        else:
            leftmost_derivations = []
            for start in list_for_start:
                derivation = Derivation(start, derive(start, [[str(start)]]))
                leftmost_derivations.append(derivation)
            return sorted(leftmost_derivations, key=lambda derivation: derivation.probability, reverse=True)


def read_PCNF(file_name):
    """
    reads from a file with name @param file_name and instantiate rules and PCNF
    for each line in the file.
    """
    fo = open(file_name, "r")
    fo_list = fo.read().splitlines()
    rules = set()
    for line in fo_list:
        rule = line.split(" ")[0]
        prob = float(line.split(" ")[1])
        left = rule.split(":")[0]
        right = []
        for char in rule.split(":")[1]:
            right.append(char)
        rules.add(PRule(left, right, prob))
    fo.close()
    return PCNF(rules)


def write_prob11_solution(input_file_name, output_file_name, string_for_derivation):
    pcnf = read_PCNF(input_file_name)
    fw = open(output_file_name, "w")
    derivations = pcnf.get_derivations(string_for_derivation)
    if derivations is None:
        print("enter")
        fw.write("Not in the language")
    else:
        for derivation in derivations:
            fw.write(str(derivation))
    fw.write("\r\n")
    fw.close()
