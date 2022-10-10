import sys
import ply.yacc as yacc
from lexer import tokens

# Reglas
def p_programa(t):
    '''
    programa : programa_1 bloque
    '''

def p_programa_1(t):
    '''
    programa_1 : vars 
        | epsilon
    '''

def p_bloque(t):
    '''
    bloque : LCURLY bloque_1 RCURLY
    '''

def p_bloque_1(t):
    '''
    bloque_1 : estatuto bloque_1 
            | epsilon
    '''

def p_vars(t):
    '''
    vars : tipo_compuesto ID vars_1 SEMICOLON vars_4
         | tipo_simple ID vars_2
    '''

def p_vars_1(t):
    '''
    vars_1 : COMMA 
           | epsilon
    '''

def p_vars_2(t):
    '''
    vars_2 : LBRACKET VAR_CONST_INT RBRACKET vars_3 SEMICLON vars_4
    '''

def p_vars_4(t):
    '''
    vars_4 : LBRACKET VAR_CONST_INT RBRACKET 
        | epsilon
    '''

def p_tipo_simple(t):
    '''
    tipo_simple : int
        | float
        | bool
        | string
    '''

def p_tipo_compuesto(t):
    '''
    tipo_compuesto : id
    '''

def p_var_const(t):
    '''
    var_const : VAR_CONST_INT
        | VAR_CONST_FLOAT
        | VAR_CONST_BOOl
        | VAR_CONST_STRING
        | id
    '''

# PENDIENTE: Revisar lo del bloque de VARS si es que es opcional
def p_funcion_void(t):
    '''
    funcion_void : FUNCTION VOID ID LPAREN params RPAREN LCURLY vars bloque RETURN exp SEMICOLON RCURLY
    '''

def p_funcion(t):
    '''
    funcion : FUNCTION tipo_simple ID LPAREN params RPAREN LCURLY vars bloque RETURN exp SEMICOLON RCURLY
    '''

def p_funcion_main(t):
    '''
    funcion_main : main LPAREN RPAREN LCURLY bloque RCURLY
    '''

def p_params(t):
    '''
    params : tipo_simple id params_1
    '''

def p_params_1(t):
    '''
    params_1 : COMMA params 
        | epsilon
    '''

# PENDIENTE: Agregar funcion especial (si es que se agregan)
def p_estatuto(t):
    '''
    estatuto : asigna
        | llamada
        | lectura
        | escritura
        | condicion
        | ciclo_w
        | ciclo_f
    '''

def p_asigna(t):
    '''
    asigna : ID ASSIGN exp SEMICOLON
    '''

def p_llamada(t):
    '''
    llamada : ID LAPREN llamada_1 RPAREN SEMICOLON
    '''

def p_llamada_1(t):
    '''
    llamada_1 : llamada_2
        | epsilon
    '''

def p_llamada_2(t):
    '''
    llamada_2 : llamada llamada_3
    '''

def p_llamada_3(t):
    '''
    llamada_3 : COMMA llamada_2
        | epsilon
    '''

def p_lectura(t):
    '''
    lectura : input CIN variable SEMICOLON
    '''

def p_escritura(t):
    '''
    escritura : output escritura_1 SEMICLON
    '''

def p_escritura_1(t):
    '''
    escritura_1 : COUT escritura_2
    '''

def p_escritura_2(t):
    '''
    escritura_2 : exp escritura_3
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
    ciclo_f : FOR LPAREN ID IN RANGE LAPREN VAR_CONST_INT COMMA VAR_CONST_INT
    '''

def p_variable(t):
    '''
    variable : ID variable_1
    '''

def p_variable_1(t):
    '''
    variable_1 : LBRACKET exp RBRACKET variable_2
    '''

def p_variable_2(t):
    '''
    variable_2 : LBRACKET exp RBRACKET variable_2
        | epsilon
    '''

def p_exp(t):
    '''
    exp : t_exp exp_1
    '''

def p_exp_1(t):
    '''
    exp_1 : OR EXP
    '''

def p_t_exp(t):
    '''
    t_exp : g_exp t_exp_1
    '''

def p_t_exp_1(t):
    '''
    t_exp_1 : AND t_exp
    '''

def p_g_exp(t):
    '''
    g_exp : m_exp g_exp_1
    '''

def p_g_exp_1(t):
    '''
    g_exp_1 : g_exp_2 m_exp
    '''

def p_g_exp_2(t):
    '''
    g_exp_2 : GREATER_THAN
        | LESS_THAN
        | GREATER_THAN_OR_EQUAL
        | LESS_THAN_OR_EQUAL
        | NOT_EQUAL
        | EQUAL
    '''

def p_m_exp(t):
    '''
    m_exp : t m_exp_1
    '''
    
def p_m_exp_1(t):
    '''
    m_exp_1 : t m_exp_2 m_exp
    '''

def p_m_exp_2(t):
    '''
    m_exp_2 : PLUS
            | MINUS
    '''
    
def p_t(t):
    '''
    t : f t_1
    '''
    
def p_t_1(t):
    '''
    t_1 : t_2 t
    '''

def p_t_2(t):
    '''
    t_2 : MULTIPLY 
        | DIVIDE 
        | MOD
    '''

def p_f(t):
    '''
    f : f_1 
      | f_2 
      | f_3 
      | f_4
    '''
    
def p_f_1(t):
    '''
    f_1 : LPAREN exp RPAREN
    '''

def p_f_2(t):
    '''
    f_2 : const_i 
        | const_f 
        | const_b 
        | const_s
    '''
    
def p_f_3(t):
    '''
    f_3 : variable
    '''
    
def p_f_4(t):
    '''
    f_4 : llamada
    '''

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