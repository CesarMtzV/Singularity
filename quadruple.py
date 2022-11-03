class Quadruple:

    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
    
    def __str__(self):
        return f"[ {self.operator} , {self.left_operand} , {self.right_operand} , {self.result} ]"
    
    def __repr__(self):
        return f"Quadruple({self.operator} , {self.left_operand} , {self.right_operand} , {self.result})"
