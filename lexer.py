import ply.lex as lex

# TOKENS
tokens = (
    'INT', 'FLOAT', 'BOOL', 'STRING', 'FUNCTION', 'VOID', 'RETURN',
    'INPUT', 'OUTPUT', 'WHILE', 'FOR', 'PI', 'IF', 'ELSE', 'SEMICOLON',
    'COLON', 'COMMA', 'LCURLY', 'RCURLY', 'ASSIGN', 'LPAREN','RPAREN',
    'LBRACKET', 'RBRACKET', 'AND', 'OR', 'CLASS', 'TRUE', 'FALSE',
    'PLUS', 'POW', 'MOD', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LESS_THAN', 'POWER',
    'COUT', 'CIN', 'MAIN', 'IN', 'RANGE', 'INHERITS', 'ATTRIBUTES', 'METHODS', 'METHOD', 'CONSTRUCTORS',
    'GREATER_THAN', 'LESS_THAN_OR_EQUAL', 'GREATER_THAN_OR_EQUAL', 'EQUAL',
    'NOT_EQUAL', 'ID', 'VAR_CONST_INT', 'VAR_CONST_FLOAT', 'VAR_CONST_STRING',
)

t_ignore = ' \t'

reserved = {
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'false': 'FALSE',
    'true': 'TRUE',
    'string': 'STRING',
    'pi': 'PI',
    'function': 'FUNCTION',
    'void': 'VOID',
    'return': 'RETURN',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'attributes': 'ATTRIBUTES',
    'methods': 'METHODS',
    'method': 'METHOD',
    'constructors': 'CONSTRUCTORS',
    'input': 'INPUT',
    'output': 'OUTPUT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'range': 'RANGE'
}

# Regular expressions rules for simple tokens
t_SEMICOLON                 = r'\;'
t_COLON                     = r'\:'
t_COMMA                     = r'\,'
t_LCURLY                    = r'\{'
t_RCURLY                    = r'\}'
t_LPAREN                    = r'\('
t_RPAREN                    = r'\)'
t_LBRACKET                  = r'\['
t_RBRACKET                  = r'\]'
t_ASSIGN                    = r'\='
t_PLUS                      = r'\+'
t_MINUS                     = r'\-'
t_MULTIPLY                  = r'\*'
t_DIVIDE                    = r'/'
t_POWER                     = r'\^'
t_MOD                       = r'%'
t_LESS_THAN                 = r'\<'
t_GREATER_THAN              = r'\>'
t_GREATER_THAN_OR_EQUAL     = r'\>\='
t_LESS_THAN_OR_EQUAL        = r'\<\='
t_COUT                      = r'\<\<'
t_CIN                       = r'\>\>'
t_EQUAL                     = r'\=\='
t_NOT_EQUAL                 = r'\!\='
t_AND                       = r'\&\&'
t_OR                        = r'\|\|'
t_VAR_CONST_STRING          = r'".*"'

def t_ID(t):
    r'[a-zA-Z]([a-zA-Z0-9])*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_VAR_CONST_INT(t):
    r'\-?[0-9]+'
    t.value = int(t.value)    
    return t

def t_VAR_CONST_FLOAT(t):
    r'\-?[0-9]+\.][0-9]+'
    t.value = float(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()