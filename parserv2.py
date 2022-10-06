import sys
import ply.yacc as yacc
from lexer import tokens

# REGLA PROGRAMA
# AGREGAR EL CUERPO DESPUES DE PROGRAMA_1
def p_programa(t):
    '''
    programa    : programa_1 
    '''

def p_programa_1(t):
    '''
    programa_1  : vars 
                | epsilon
    '''

# REGLA VARS

def p_vars(t):
    '''
    vars        : tipo_simple ID vars_1
                | tipo_compuesto ID SEMICOLON vars_4
    '''

def p_vars_1(t):
    '''
    vars_1      : SEMICOLON vars_4
                | vars_2
    '''

def p_vars_2(t):
    '''
    vars_2      : LBRACKET VAR_CONST_INT RBRACKET vars_3
    '''

def p_vars_3(t):
    '''
    vars_3      : LBRACKET VAR_CONST_INT RBRACKET SEMICOLON vars_4 
                | SEMICOLON vars_4
    '''

def p_vars_4(t):
    '''
    vars_4      : vars 
                | epsilon
    '''

# REGLA TIPOS DE DATOS

def p_tipo_simple(t):
    '''
    tipo_simple : INT 
                | FLOAT 
                | BOOL 
                | STRING
    '''

def p_tipo_compuesto(t):
    '''
    tipo_compuesto : ID
    '''

# REGLA CUERPO

# def p_cuerpo(t):
#     '''
#     cuerpo      :  cuerpo_1 funcion_main
#     '''

# def p_cuerpo_1(t):
#     '''
#     cuerpo_1    : funciones 
#                 | epsilon
#     '''

# REGLAS FUNCIONES (FALTA AGREGAR EL BLOQUE ENTRE LOS CURLY BRACKETS)
# def p_funcion_main(t):
#     '''
#     funcion_main: MAIN LPAREN RPAREN LCURLY RCURLY
#     '''

# def p_funciones(t):
#     '''
#     funciones   : funcion_tipo funciones_1
#                 | funcion_void funciones_1
#     '''

# def p_funciones_1(t):
#     '''
#     funciones_1 : funciones
#                 | epsilon
#     '''

# # FALTA AGREGAR EL BLOQUE ENTRE LOS CURLY BRACKETS
# def p_funcion_tipo(t):
#     '''
#     funcion_tipo: FUNCTION tipo_simple ID LPAREN params RPAREN LCURLY RETURN RCURLY
#     '''

# def p_funcion_void(t):
#     '''
#     funcion_void: FUNCTION VOID ID LPAREN params RPAREN LCURLY RCURLY
#     '''

# # REGLA PARAMS
# def p_params(t):
#     '''
#     params      : tipo_simple ID params_1
#     '''

# def p_params_1(t):
#     '''
#     params_1    : COMMA params
#                 | epsilon
#     '''

def p_epsilon(t):
    'epsilon :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        program_file = sys.argv[1]

        with open(sys.argv[1], 'r') as f:
            data = f.read()
            yacc.parse(data)
            print("Parser finished reading the file.")