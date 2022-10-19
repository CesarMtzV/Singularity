from semanticCube import SemanticCube

class ICG:
    def __init__(self):
        self.quadrupleList = []
        self.stackOperands = []
        self.stackOperators = []
        self.stackTypes = []
        self.stackJumps = []
        self.semanticCube = SemanticCube()
        
        