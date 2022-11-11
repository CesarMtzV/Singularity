class Quadruple:

    def __init__(self, ip_counter :int, operator, left_operand :int, right_operand :int, result :int):
        self.ip_counter = ip_counter # Instruction Pointer
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
    
    def __str__(self):
        return f"[ {self.ip_counter} , {self.operator} , {self.left_operand} , {self.right_operand} , {self.result} ]"
    
    def __repr__(self):
        return f"Quadruple({self.operator} , {self.left_operand} , {self.right_operand} , {self.result})"
