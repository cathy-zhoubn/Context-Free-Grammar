"""
PROBLEM 12, helpers
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
        self.unary = set()
        self.binary = set()
        for rule in self.rules:
            if len(rule.getRight()) == 1:
                self.unary.add(rule)
            else:
                self.binary.add(rule)

    def initialize_prob(self):
        """
        givin a @param pcnf of class PCNF without probability, initialize
        probability uniformly so that for each nonterminal V, the sum of all
        its rules equals 1.
        """
        nonterm_rules = {}
        for nonterm in self.get_nonterminals():
            nonterm_rules[nonterm] = []
        for rule in self.get_rules():
            nonterm_rules[rule.getLeft()].append(rule)
        for nonterm_key in nonterm_rules:
            count = len(nonterm_rules[nonterm_key])
            for rule in nonterm_rules[nonterm_key]:
                rule.prob = 1/count

    def inside(self, string):
        """
        uses the inside algorithm to output inside probability matrix for given
        string
        """
        str_len = len(string)
        table = []
        for i in range(str_len):  # initializes the array
            table.append([])
            for j in range(str_len):
                table[i].append({})

        for i in range(str_len):  # calculate the fist row of the array
            for rule in self.unary:
                right = rule.getRight()
                if right[0] == string[i]:
                    table[i][i][rule.getLeft()] = rule.getProb()

        for length in range(1, str_len+1):  # performs update
            for span in range(str_len-length):
                for rule in self.binary:
                    right1 = rule.getRight()[0]
                    right2 = rule.getRight()[1]
                    left = rule.getLeft()
                    sum = 0
                    for partition in range(length):
                        index1 = table[span][span + partition]
                        index2 = table[span + partition+1][span+length]
                        if right1 in index1.keys() and right2 in index2.keys():
                            sum += rule.getProb()*index1[right1]*index2[right2]
                    if sum > 0:
                        if left in table[span][span+length]:
                            table[span][span+length][left] += sum
                        else:
                            table[span][span+length][left] = sum
        return table

    def outside(self, inside_table, string):
        """
        uses the outside algorithm to output outside probability matrix for given
        string
        """
        str_len = len(string)
        table = []
        for i in range(str_len):  # initializes the array
            table.append([])
            for j in range(str_len):
                table[i].append({})

        table[0][-1]["S"] = 1.0  # initializing step

        for length in reversed(range(str_len-1)):  # performs update
            for span in range(str_len-length):
                for rule in self.binary:
                    right1 = rule.getRight()[0]
                    right2 = rule.getRight()[1]
                    left = rule.getLeft()
                    sum1 = 0
                    for partition in range(length+span+1, str_len):
                        inside1 = inside_table[span+length+1][partition]
                        outside1 = table[span][partition]
                        if right2 in inside1.keys() and left in outside1.keys():
                            sum1 += rule.getProb()*inside1[right2]*outside1[left]
                    if sum1 > 0:
                        if right1 in table[span][length+span]:
                            table[span][length+span][right1] += sum1
                        else:
                            table[span][length+span][right1] = sum1
                    sum2 = 0
                    for partition in range(span):
                        inside2 = inside_table[partition][span-1]
                        outside2 = table[partition][span+length]
                        if right1 in inside2.keys() and left in outside2.keys():
                            sum2 += rule.getProb()*inside2[right1]*outside2[left]
                    if sum2 > 0:
                        if right2 in table[span][length+span]:
                            table[span][length+span][right2] += sum2
                        else:
                            table[span][length+span][right2] = sum2
        return table

    def update_rules(self, string_list):
        inside_prob_list = []
        outside_prob_list = []
        updated_rules = []
        for string in string_list:
            inside_prob = self.inside(string)
            outside_prob = self.outside(inside_prob, string)
            inside_prob_list.append(inside_prob)
            outside_prob_list.append(outside_prob)

        for rule in self.rules:
            left = rule.getLeft()
            sum_nonterm = 0  # C(i | O), total expected cases
            sum_rule = 0
            for string_num in range(len(string_list)):
                string = string_list[string_num]
                str_len = len(string)
                outside_prob = outside_prob_list[string_num]
                inside_prob = inside_prob_list[string_num]
                for i in range(str_len):
                    for j in range(i, str_len):
                        out_index = outside_prob[i][j]
                        in_index = inside_prob[i][j]
                        if left in out_index.keys() and left in in_index.keys():
                            sum_nonterm += out_index[left] * in_index[left]/inside_prob[0][-1]["S"]

                # C(i → jk, i | O), expected number of rules used given nonterminal i
                if rule in self.binary:
                    right1 = rule.getRight()[0]
                    right2 = rule.getRight()[1]
                    for i in range(str_len-1):
                        for j in range(i + 1, str_len):
                            out_index = outside_prob[i][j]
                            if left in out_index.keys():
                                temp_sum = 0
                                for k in range(i, j):
                                    index1 = inside_prob[i][k]
                                    index2 = inside_prob[k+1][j]
                                    if right1 in index1.keys() and right2 in index2.keys():
                                        temp_sum += index1[right1] * index2[right2]
                                sum_rule += rule.getProb() * temp_sum * \
                                    out_index[left]/inside_prob[0][-1]["S"]

                else:  # C(i → x, i | O) where x is terminal
                    right = rule.getRight()[0]
                    for i in range(str_len):
                        if string[i] == right:
                            in_index = inside_prob[i][i]
                            out_index = outside_prob[i][i]
                            if left in in_index.keys() and left in out_index.keys():
                                sum_rule += in_index[left] * out_index[left]/inside_prob[0][-1]["S"]

            if sum_nonterm == 0:
                updated_rules.append(rule)
            else:
                updated_rules.append(PRule(left, rule.getRight(), sum_rule/sum_nonterm))
        return updated_rules

    def is_local_optimum(self, updated_rules, deviation):
        max_deviation = 0
        for rule1 in self.rules:
            for rule2 in updated_rules:
                if rule1.getLeft() == rule2.getLeft() and rule1.getRight() == rule2.getRight():
                    max_deviation = max(abs(rule1.getProb()-rule2.getProb()), max_deviation)
        return max_deviation < deviation

    def inside_outside(self, string_list, deviation):
        self.initialize_prob()
        pcnf = copy.deepcopy(self)
        updated_rules = pcnf.update_rules(string_list)
        while not pcnf.is_local_optimum(updated_rules, deviation):
            pcnf = PCNF(copy.deepcopy(updated_rules))
            updated_rules = PCNF(updated_rules).update_rules(string_list)
        return pcnf


def read_PCNF_without_prob(file_name):
    """
    reads from a file with name @param file_name and instantiate rules and PCNF
    with each probability as None for each line in the file.
    """
    fo = open(file_name, "r")
    fo_list = fo.read().splitlines()
    rules = set()
    for line in fo_list:
        prob = None
        left = line.split(":")[0]
        right = []
        for char in line.split(":")[1]:
            right.append(char)
        rules.add(PRule(left, right, prob))
    fo.close()
    return PCNF(rules)


def read_strings(file_name):
    """
    read the file containing all strings and returns them as list
    """
    string_list = []
    fo = open(file_name, "r")
    fo_list = fo.read().splitlines()
    for line in fo_list:
        for string in line.split(" "):
            string_as_list = []
            for char in string:
                string_as_list.append(char)
            string_list.append(string_as_list)
    fo.close()
    return string_list


def write_prob12_solution(grammar_file_name, string_file_name, output_file_name):
    pcnf = read_PCNF_without_prob(grammar_file_name)
    strings = read_strings(string_file_name)
    DEVIATION = 0.001
    pcnf = pcnf.inside_outside(strings, DEVIATION)
    fw = open(output_file_name, "w")
    for rule in pcnf.get_rules():
        fw.write(str(rule)+"\n")
    fw.write("\r\n")
    fw.close()
