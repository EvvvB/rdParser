import re
from functools import *

"""
Pair Programmer 1 - Evan Ballesteros 823103028
Pair Programmer 2 - Lisa Casas 821405917


We the undersigned promise that we have in good faith attempted to follow 
the principles of pair programming. Although we were free to discuss ideas 
with others, the implementation is our own. We have shared a common workspace 
and taken turns at the keyboard for the majority of the work that we are 
submitting. Furthermore, any non programming portions of the assignment were
 done independently. We recognize that should this not be the case, we will 
 be subject to penalties as outlined in the course syllabus.

A LL recursive descent parser for validating simple expressions.

You would need to first write the grammar rules (non-terminal) in EBNF according to the token
patterns and grammar rules specified in Assignment 2 Task A. 
You can then follow the examples of the parsing procedure pseudocode implementation in Figure 5.17
in the textbook to write the recursive descent parsing procedures for the validation parsing.

The following recursive descent parsing algorithm is a LL parser. It implements one parsing 
procedure for each one of the above non-terminals (grammar rules), starting from the top of the 
parse tree, then drilling into lower hierachical levels.

The procedures work together to handle all combinations of the grammar rules, and they 
automatically handle the nested compositions of terms with multi-level priority brackets. 

---------------------------------------------------------------------
Usage

r = recDecsent('7 - 17')
print(r.validate()) # will print True as '7 - 17' is a valid expression

r = recDecsent('7 - ')
print(r.validate()) # will print False as '7 - ' is an invalid expression

"""

class recDescent:
    
    # relational (unary) operators (
    relop = ['<', '>', '<=', '>=', '=', '!=', 'not']
    
    # binary operators (infix)
    dashop = ['-', '–']
    logicop = ['and', 'or']

    # tokens for manipulating priority
    priopen = '('
    priclose = ')'

    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):

        # string to be parsed
        self.expr = expr

        # tokens from lexer tokenization of the expression
        self.tokens = []

    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    # do not edit any piece of code in this function
    def lex(self):
        self.tokens = re.findall("[-\(\)=]|[!<>]=|[<>]|\w+|[^ +]\W+", self.expr)
        # filter out the possible spaces in the elements
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    
    
    # parser - determine if the input expression is valid or not
    
    # validate() function will return True if the expression is valid, False otherwise 
    # do not change the method signature as this function will be called by the autograder
    def check_len(self, ptr):
        return ptr < len(self.tokens)

    #runs first expression call
    def validate(self):
        self.lex()
        ptr = 0
        (result, ptr) = self.expression_validator(ptr)
        return result

    # use your parsing procedures below to validate -------------------

    def expression_validator(self, ptr):
        # print("expression" + str(ptr))

        #check for single/first term
        first_term = self.term_validator(ptr)
        ptr = first_term[1]

        subsiq_terms = 0
        is_op = True

        #check for subsiquent terms
        while self.check_len(ptr) and is_op:
            is_op = False
            if self.tokens[ptr] in self.logicop:
                subsiq_terms += 1
                ptr += 1
                is_op = True
                if self.check_len(ptr):
                    next_term = self.term_validator(ptr)
                    ptr = next_term[1]
                    # print(next_term[0])
                    if next_term[0]:
                        subsiq_terms += 1

        #be sure subsiquent terms have both "and" and also a term
        if first_term[0] and ((subsiq_terms % 2) == 0):
            valid_and_ptr = (True, ptr)
        else:
            valid_and_ptr = (False, ptr)

        return valid_and_ptr


    def term_validator(self, ptr):
        # print("term" + str(ptr))
        valid_and_ptr = (False, ptr)

        #check for first numeric (num - num)
        if self.check_len(ptr) and self.tokens[ptr].isnumeric():
            ptr += 1
            if self.check_len(ptr) and self.tokens[ptr] in self.dashop:
                ptr += 1
                if self.check_len(ptr) and self.tokens[ptr].isnumeric():
                    ptr += 1
                    valid_and_ptr = (True, ptr)

        #check for first "(" ( <expression> )
        elif self.check_len(ptr) and self.tokens[ptr] in self.priopen:
            ptr += 1
            valid_expr = self.expression_validator(ptr)
            ptr = valid_expr[1]
            if valid_expr[0]:
                if self.check_len(ptr) and self.tokens[ptr] in self.priclose:
                    ptr += 1
                    valid_and_ptr = (True, ptr)

        #check for first relop <relop> numeric
        elif self.check_len(ptr):
            isRelop = self.relational_validator(ptr)
            if isRelop:
                ptr += 1
                if self.check_len(ptr) and self.tokens[ptr].isnumeric():
                    valid_and_ptr = (True, ptr + 1)
        # print(valid_and_ptr)
        return valid_and_ptr


    #method to check for relop token
    def relational_validator(self, ptr):
        # print("relation" + str(ptr))
        validated = False

        if self.check_len(ptr) and self.tokens[ptr] in self.relop:
            validated = True

        return validated

# parsing procedures corresponding to the grammar rules - follow Figure 5.17

# something = recDescent("((((>= 1 or (1-4)))")
# something = recDescent("(1 - 100 or (> 100 and < 150)) and != 100")

# print(something.tokens)
# print(something.validate())
