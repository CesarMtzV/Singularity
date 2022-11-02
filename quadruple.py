import string

import sys

class Quadruple:
  
    def __init__(self, operator, left_operator, right_operator, result):
        self.operator = operator
        self.left_operator = left_operator
        self.right_operator = right_operator
        self.result = result

    def generate_quad(self, op, left_op, right_op, res):
        self.id += 1
        quad = Quadruple(self.id, op, left_op, right_op, res)
        return quad

    def print_quad(self):
        print("[" + str(self.operator) + "," + str(self.left_operator) + "," + str(self.right_operator) + "," + str(self.result) + "]")
