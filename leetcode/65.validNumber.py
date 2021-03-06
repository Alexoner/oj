# -*- coding: utf-8 -*-
'''
65. Valid Number

Validate if a given string is numeric.

Some examples:

"0" => true

" 0.1 " => true

"abc" => false

"1 a" => false

"2e10" => true

Note: It is intended for the problem statement to be ambiguous. You
should gather all requirements up front before implementing one.


==============================================================================================
SOLUTION

1. Naive solution
Case by case analysis.

1) Beginning and trailing white spaces can be left out
2) The most complex situation is when a number is in scientific
notation:
    <float number>e<integer>

AeB or AEB represents A * 10 ^ B
A can be a decimal or integer，maybe with sign(+-)
.35, 00. are valid decimal
'.' is invalid number

B must be an integer，with or without sign
If there is 'e', both A and B must exist.

@2 FINITE STATE MACHINE (DETERMINISTIC FINITE AUTOMATA)

Hard-code the rules can be error prune prone, because this problem comprises many
states, and a state can move to another state, following the rule. And it reveals
a GRAPH structure, more precisely, FINITE STATE MACHINE.

Refer to CLRS for more information about string matching with FINITE AUTOMATA.

To construct a finite automata transition diagram. States can be classified into:
    0:initial state
    1:sign
    2:digit
    3:point
    4:point and digit
    5:'e' or 'E'
    6:sign after 'e' or 'E'
    7:digit after 5
    8:space after 7

Construct the state transition function/table. Process the characters one by one,
moving state according to the state transition function.

'''


class Solution:
    # @param s, a string
    # @return a boolean

    def isNumber(self, s):
        state = 0
        for i in range(0, len(s)):
            state = self.nextState(state, s[i])
            if state == -1:
                return False
        # To finish the state transition manually
        state = self.nextState(state, ' ')
        return state == 8

    def nextState(self, state, char):
        # STATE TRANSITION MATRIX FOR THE DETERMINISTIC FINITE AUTOMATA
        #               0 space, 1 digit, 2 sign, 3 dot, 4 e, 5 il
        transititionTable = [[0, 2, 1, 3, -1, -1],  # 0
                             [-1, 2, -1, 3, -1, -1],  # 1
                             [8, 2, -1, 4, 5, -1],  # 2
                             [-1, 4, -1, -1, -1, -1],  # 3
                             [8, 4, -1, -1, 5, -1],  # 4
                             [-1, 7, 6, -1, -1, -1],  # 5
                             [-1, 7, -1, -1, -1, -1],  # 6
                             [8, 7, -1, -1, -1, -1],  # 7
                             [8, -1, -1, -1, -1, -1]]  # 8
        return transititionTable[state][self.getSymbol(char)]

    def getSymbol(self, char):
        if char == ' ' or char == '\t':
            return 0
        elif char.isdigit():
            return 1
        elif char == '+' or char == '-':
            return 2
        elif char == '.':
            return 3
        elif char == 'E' or char == 'e':
            return 4
        return 5

if __name__ == "__main__":
    print("-.5364764e+3 is %s" % Solution().isNumber("-.5364764e+3"))
    print("-34342.e-3 is %s" % Solution().isNumber("-34342.e-3"))
