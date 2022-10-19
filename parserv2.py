from operator import ge
import sys
import ply.yacc as yacc
from Quadruple import Quadruple

from lexer import tokens
from varsTable import VariablesTable
from IntermediateCodeGen import ICG
from semanticCube import SemanticCube
from Quadruple import Quadruple

vars_table = VariablesTable()
generateIC = ICG()
SemanticCube = SemanticCube()
generateQuad = []

# REGLA PROGRAMA
def p_programa(t):
    '''
    programa    : programa_1 cuerpo
    '''

def p_programa_1(t):
    '''
    programa_1  : vars 
                | epsilon
    '''

# REGLA CUERPO

def p_cuerpo(t):
    '''
    cuerpo      :  cuerpo_1 funcion_main
    '''

def p_cuerpo_1(t):
    '''
    cuerpo_1    : np_end_global_scope funciones 
                | epsilon
    '''

# REGLA VARS

def p_vars(t):
    '''
    vars        : tipo_simple ID np_add_variable vars_1
                | tipo_compuesto ID np_add_variable SEMICOLON vars_4
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

# REGLAS FUNCIONES (FALTA AGREGAR EL BLOQUE ENTRE LOS CURLY BRACKETS)
def p_funcion_main(t):
    '''
    funcion_main : MAIN LPAREN RPAREN LCURLY bloque RCURLY
    '''
    print(vars_table.vars_table)

def p_funciones(t):
    '''
    funciones   : funcion_tipo funciones_1
                | funcion_void funciones_1
    '''

def p_funciones_1(t):
    '''
    funciones_1 : funciones
                | epsilon
    '''

# # FALTA AGREGAR EL BLOQUE ENTRE LOS CURLY BRACKETS
def p_funcion_tipo(t):
    '''
    funcion_tipo : FUNCTION tipo_simple ID np_add_function LPAREN params RPAREN LCURLY bloque RETURN RCURLY
    '''

def p_funcion_void(t):
    '''

    funcion_void : FUNCTION VOID ID np_add_function LPAREN params RPAREN LCURLY bloque RCURLY
    '''

# REGLA PARAMS
def p_params(t):
    '''
    params      : tipo_simple ID np_function_parameters params_1 
                | epsilon
    '''

def p_params_1(t):
    '''
    params_1    : COMMA params
                | epsilon
    '''

def p_bloque(t):
    '''
    bloque      : estatuto bloque_1
    '''

def p_bloque_1(t):
    '''
    bloque_1    : bloque
                | epsilon
    '''

# TODO: EL RESTO DE LOS ESTATUTOS
def p_estatuto(T):
    '''
    estatuto    : asigna
                | llamada
                | lectura
                | escritura
                | condicion
                | ciclo_w
                | ciclo_f
    '''

# TODO: ID puede ser un arreglo, una matriz, atributo de una clase, etc... Hay que adaptarlo
def p_asigna(t):
    '''
    asigna      : ID ASSIGN exp SEMICOLON
    '''

def p_llamada(t):
    '''
    llamada     : ID LPAREN llamada_1 RPAREN SEMICOLON
    '''

def p_llamada_1(t):
    '''
    llamada_1   : llamada_2
                | epsilon
    '''

def p_llamada_2(t):
    '''
    llamada_2   : exp llamada_3
    '''

def p_llamada_3(t):
    '''
    llamada_3   : COMMA llamada_2
                | epsilon
    '''

def p_lectura(t):
    '''
    lectura : INPUT CIN variable SEMICOLON
    '''

def p_escritura(t):
    '''
    escritura : OUTPUT escritura_1 SEMICOLON
    '''

def p_escritura_1(t):
    '''
    escritura_1 : COUT escritura_2 escritura_3
    '''

def p_escritura_2(t):
    '''
    escritura_2 : exp
                | VAR_CONST_STRING
    '''

def p_escritura_3(t):
    '''
    escritura_3 : escritura_1
                | epsilon
    '''

def p_condicion(t):
    '''
    condicion : IF LPAREN exp RPAREN LCURLY bloque RCURLY condicion_1
    '''

def p_condicion_1(t):
    '''
    condicion_1 : ELSE LCURLY bloque RCURLY
                | epsilon
    '''

def p_ciclo_w(t):
    '''
    ciclo_w : WHILE LPAREN exp RPAREN LCURLY bloque RCURLY
    '''

def p_ciclo_f(t):
    '''
    ciclo_f : FOR LPAREN ID IN RANGE LPAREN VAR_CONST_INT COMMA VAR_CONST_INT RPAREN RPAREN LCURLY bloque RCURLY
    '''

# REGLA DE EXPRESION
def p_exp(t):
    '''
    exp         : t_exp exp_1
    '''

def p_exp_1(t):
    '''
    exp_1       : OR exp
                | epsilon
    '''

# REGLA DE TERA EXPRESION
def p_t_exp(t):
    '''
    t_exp       : g_exp t_exp_1
    '''

def p_t_exp_1(t):
    '''
    t_exp_1     : AND t_exp
                | epsilon
    '''

# REGLA DE GIGA EXPRESION
def p_g_exp(t):
    '''
    g_exp       : m_exp np_expression g_exp_1
    '''

def p_g_exp_1(t):
    '''
    g_exp_1     : g_exp_2 m_exp
                | epsilon
    '''

def p_g_exp_2(t):
    '''
    g_exp_2     : GREATER_THAN
                | LESS_THAN
                | GREATER_THAN_OR_EQUAL
                | LESS_THAN_OR_EQUAL
                | NOT_EQUAL
                | EQUAL np_add_operator
    '''

# REGLAS DE MEGA EXPRESION
def p_m_exp(t):
    '''
    m_exp       : termino m_exp_1
    '''

def p_m_exp_1(t):
    '''
    m_exp_1     : PLUS m_exp
                | MINUS m_exp
                | epsilon
    '''

# REGLAS DE TERMINO
def p_termino(t):
    '''
    termino     : factor termino_1
    '''

def p_termino_1(t):
    '''
    termino_1   : MULTIPLY termino
                | DIVIDE termino
                | MOD termino
                | epsilon
    '''

# REGLAS DE FACTOR
def p_factor(t):
    '''
    factor      : factor_1 factor_2 factor_3 factor_4
    '''

def p_factor_1(t):
    '''
    factor_1    : LPAREN exp RPAREN
                    | epsilon
    '''

def p_factor_2(t):
    '''
    factor_2    : VAR_CONST_INT
                | VAR_CONST_FLOAT
                | VAR_CONST_STRING
                | FALSE
                | TRUE
                | epsilon
    '''

def p_factor_3(t):
    '''
    factor_3    : variable
                | epsilon
    '''

def p_factor_4(t):
    '''
    factor_4    : llamada
                | epsilon
    '''

# REGLAS DE VARIABLE
def p_variable(t):
    '''
    variable    : ID variable_1
    '''

def p_variable_1(t):
    '''
    variable_1  : LBRACKET exp RBRACKET variable_2
                | epsilon
    '''

def p_variable_2(t):
    '''
    variable_2  : LBRACKET exp RBRACKET
                | epsilon
    '''

def p_epsilon(t):
    'epsilon : '
    pass

def p_error(t):
    if not t:
        print("Syntax error: Unexpected END OF FILE")
    else:
        print(f"Syntax error: Unexpected {t.type}({t.value}) on line {t.lineno} ")


##########################
### PUNTOS NEURALGICOS ###
##########################

# Adding a function to the functions directory
def p_np_add_function(p):
    'np_add_function :'
    vars_table.add_function(p)

# Adding a function's parameters to its symbol table
def p_np_function_parameters(p):
    'np_function_parameters :'
    vars_table.add_function_parameters(p)
        
# Adding a variable to the symbols table
def p_np_add_variable(p):
    'np_add_variable :'
    vars_table.add_variable(p)

def p_np_end_global_scope(p):
    'np_end_global_scope :'
    vars_table.global_scope = False
    
def p_np_add_operator(p):
    'np_add_operator :'

    generateIC.stackOperands.append(p[1])

# Handle expressions
def p_np_expression(p):
    'np_expression :'

    if (generateIC.stackOperators):
        operator = generateIC.stackOperators[-1]
        if operator == '>' or operator == '>=' or operator == '<' or operator == '<=' or operator == '==' or operator == '<>':
            right = generateIC.stackOperands.pop()
            left = generateIC.stackOperands.pop()
            rightType = generateIC.stackTypes.pop()
            leftType = generateIC.stackTypes.pop()
            operator = generateIC.stackOperators.pop()
            resultType = SemanticCube[leftType][rightType][operator]

            if resultType == 'error':
                print(f'Cannot perform \'{operator}\' with \'{leftType}\' and \'{rightType}\' as operands!')
            else:
                
                generateQuad.append(Quadruple(left,right,operator, ))
                generateIC.stackTypes.append(resultType)
                idx += 1
        
yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        program_file = sys.argv[1]

        with open(sys.argv[1], 'r') as f:
            data = f.read()
            yacc.parse(data)
            print("Parser finished reading the file.")