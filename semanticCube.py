class SemanticCube():
    def __init__(self):
        self.semantic_cube={
            'int': {
                'int': {
                    '+': 'int',
                    '-': 'int',
                    '*': 'int',
                    '/': 'int',
                    '%': 'int',
                    '^': 'int',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'float': {  
                    '+': 'float',
                    '-': 'float',
                    '*': 'float',
                    '/': 'float',
                    '%': 'float',
                    '^': 'float',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'bool': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'string': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'pointer': {
                    '+': 'int',
                    '-': 'int',
                    '*': 'int',
                    '/': 'int',
                    '%': 'int',
                    '^': 'int',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                }

            },
            'float': {
                'int': {
                    '+': 'float',
                    '-': 'float',
                    '*': 'float',
                    '/': 'float',
                    '%': 'float',
                    '^': 'float',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'float': {
                    '+': 'float',
                    '-': 'float',
                    '*': 'float',
                    '/': 'float',
                    '%': 'float',
                    '^': 'float',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'bool': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'string': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'pointer': {
                    '+': 'float',
                    '-': 'float',
                    '*': 'float',
                    '/': 'float',
                    '%': 'float',
                    '^': 'float',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
            },
            'bool': {
                'int': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'float': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'bool': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'bool',
                    '||': 'bool'
                },
                'string': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'pointer': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'bool',
                    '||': 'bool'
                },
            },
            'string': {
                'int': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'float': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'bool': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'string': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'pointer': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '%': 'error',
                    '^': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                }
            },
            'pointer': {
                'int': {
                    '+': 'int',
                    '-': 'int',
                    '*': 'int',
                    '/': 'int',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'float': {
                    '+': 'float',
                    '-': 'float',
                    '*': 'float',
                    '/': 'float',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                },
                'bool': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'bool',
                    '||': 'bool'
                },
                'string': {
                    '+': 'error',
                    '-': 'error',
                    '*': 'error',
                    '/': 'error',
                    '>': 'error',
                    '>=': 'error',
                    '<': 'error',
                    '<=': 'error',
                    '==': 'error',
                    '!=': 'error',
                    '&&': 'error',
                    '||': 'error'
                },
                'pointer': {
                    '+': 'pointer',
                    '-': 'pointer',
                    '*': 'pointer',
                    '/': 'pointer',
                    '>': 'bool',
                    '>=': 'bool',
                    '<': 'bool',
                    '<=': 'bool',
                    '==': 'bool',
                    '!=': 'bool',
                    '&&': 'error',
                    '||': 'error'
                }
            }
        }