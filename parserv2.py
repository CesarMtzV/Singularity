import sys
from pprint import pprint
import ply.yacc as yacc

from lexer import tokens
from varsTable import VariablesTable, VarsTableException
from quadruple import Quadruple
from semanticCube import SemanticCube
from MemoryManager import MemoryManager

vars_table = VariablesTable()
semantic_cube = SemanticCube().semantic_cube 
memory = MemoryManager()

temp = {}

## Se guardan los operadoes como + - * / y los GOTOS GOTOF GOTOV
stack_operators = []
##se guardan las cosas con las que opero que son los IDs
stack_operands = []
## Se guardan los tipos
stack_types = []
# Se guardan los saltos
stack_jumps = []

##Se guardan los cuadruplos que se van generando
quad_list = []

is_void_function = False

################
### PROGRAMA ###
################
def p_programa(t):
    '''
    programa    : programa_1 cuerpo
    '''

def p_programa_1(t):
    '''
    programa_1  : vars 
                | epsilon
    '''


##############
### CUERPO ###
##############
def p_cuerpo(t):
    '''
    cuerpo      :  cuerpo_2 cuerpo_1 np_end_global_scope funcion_main
    '''

def p_cuerpo_1(t):
    '''
    cuerpo_1    : funciones 
                | epsilon
    '''

def p_cuerpo_2(t):
    '''
    cuerpo_2    : clase
                | epsilon
    '''


############
### VARS ###
############
def p_vars_sup(t):
    '''
    vars_sup    : vars 
                | epsilon
    '''
    
def p_vars(t):
    '''
    vars        : tipo_simple ID np_add_variable vars_1
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


######################
### TIPOS DE DATOS ###
######################
def p_tipo_simple(t):
    '''
    tipo_simple : INT 
                | FLOAT 
                | BOOL 
                | STRING
    '''
    vars_table.current_type = t[1]

#################
### FUNCIONES ###
#################
def p_funcion_main(t):
    '''
    funcion_main : MAIN LPAREN RPAREN LCURLY bloque RCURLY
    '''

def p_funciones(t):
    '''
    funciones   : funcion funciones
                | epsilon
    '''

def p_function(t):
    '''
    funcion     : FUNCTION VOID ID np_add_void_function LPAREN params RPAREN LCURLY vars_sup bloque RCURLY 
                | FUNCTION tipo_simple ID np_add_function LPAREN params RPAREN LCURLY vars_sup bloque RCURLY
                | epsilon
    '''


##############
### PARAMS ###
##############
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


##############
### BLOQUE ###
##############
def p_bloque(t):
    '''
    bloque      : estatuto bloque
                | epsilon
    '''


#################
### ESTATUTOS ###
#################
def p_estatuto(T):
    '''
    estatuto    : asigna
                | llamada
                | lectura
                | escritura
                | condicion
                | ciclo_w
                | ciclo_f
                | return
    '''

# TODO: ID puede ser un arreglo, una matriz, atributo de una clase, etc... Hay que adaptarlo
def p_asigna(t):
    '''
    asigna      : ID np_add_operand ASSIGN np_add_operator exp SEMICOLON
    '''
    operator = stack_operators.pop()
    operand = stack_operands.pop()
    result = stack_operands.pop()

    quad_list.append(Quadruple(operator, operand, None, result))


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
    lectura : INPUT np_add_operator CIN variable SEMICOLON
    '''
    operator = stack_operators.pop()
    operand = stack_operands.pop()

    quad_list.append(Quadruple(operator, None, None, operand))

def p_escritura(t):
    '''
    escritura : OUTPUT escritura_1 SEMICOLON
    '''
    

def p_escritura_1(t):
    '''
    escritura_1 : COUT np_add_write_operator escritura_2 escritura_3
    '''
    operator = stack_operators.pop()
    operand = stack_operands.pop()

    quad_list.append(Quadruple(operator, None, None, operand))

def p_escritura_2(t):
    '''
    escritura_2 : exp
                | VAR_CONST_STRING np_add_string
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

def p_return(t):
    '''
    return  : RETURN np_add_operator exp SEMICOLON
    '''
    operator = stack_operators.pop()
    operand = stack_operands.pop()

    quad_list.append(Quadruple(operator, None, None, operand))

##############
### CLASES ###
##############

def p_clase(t):
    '''
    clase       : CLASS ID LCURLY ATTRIBUTES COLON vars constructor metodos RCURLY clase
                | CLASS ID INHERITS ID LCURLY ATTRIBUTES COLON vars constructor metodos RCURLY clase
                | epsilon
    '''

def p_constructor(t):
    '''
    constructor : CONSTRUCTORS COLON constructores
    '''

def p_constructores(t):
    '''
    constructores   : ID LPAREN RPAREN LCURLY bloque RCURLY constructores
                    | ID LPAREN params RPAREN LCURLY bloque RCURLY constructores
                    | epsilon
    '''

def p_metodos(t):
    '''
    metodos     : METHODS COLON metodo
    '''

def p_metodo(t):
    '''
    metodo      : METHOD tipo_simple ID LPAREN params RPAREN LCURLY bloque RCURLY metodo
                | METHOD VOID ID LPAREN params RPAREN LCURLY bloque RCURLY metodo
                | epsilon
    '''


#################
### EXPRESION ###
#################
def p_exp(t):
    '''
    exp         : t_exp np_add_or exp_1
    '''

def p_exp_1(t):
    '''
    exp_1       : OR np_add_operator exp
                | epsilon
    '''

# REGLA DE TERA EXPRESION
def p_t_exp(t):
    '''
    t_exp       : g_exp np_add_and t_exp_1
    '''

def p_t_exp_1(t):
    '''
    t_exp_1     : AND np_add_operator t_exp
                | epsilon
    '''

# REGLA DE GIGA EXPRESION
def p_g_exp(t):
    '''
    g_exp       : m_exp np_add_conditionals g_exp_1
    '''

def p_g_exp_1(t):
    '''
    g_exp_1     : g_exp_2
                | epsilon
    '''

def p_g_exp_2(t):
    '''
    g_exp_2     : GREATER_THAN np_add_operator g_exp
                | LESS_THAN np_add_operator g_exp
                | GREATER_THAN_OR_EQUAL np_add_operator g_exp
                | LESS_THAN_OR_EQUAL np_add_operator g_exp
                | NOT_EQUAL np_add_operator g_exp
                | EQUAL np_add_operator g_exp
    '''

# REGLAS DE MEGA EXPRESION
def p_m_exp(t):
    '''
    m_exp       : termino np_add_plusminus m_exp_1
    '''

def p_m_exp_1(t):
    '''
    m_exp_1     : PLUS np_add_operator m_exp
                | MINUS np_add_operator m_exp
                | epsilon
    '''

# REGLAS DE TERMINO
def p_termino(t):
    '''
    termino     : factor np_add_multiplydivision termino_1
    '''

def p_termino_1(t):
    '''
    termino_1   : MULTIPLY np_add_operator termino
                | DIVIDE np_add_operator termino
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
    factor_2    : VAR_CONST_INT np_add_int
                | VAR_CONST_FLOAT np_add_float
                | VAR_CONST_STRING np_add_string
                | FALSE np_add_bool
                | TRUE np_add_bool
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
    variable    : ID np_add_operand variable_1
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
    vars_table.add_function(p[-1], False) # p[-1] = nombre_funcion
    pass

def p_np_add_void_function(p):
    'np_add_void_function :'
    vars_table.add_function(p[-1], True) # p[-1] = nombre_funcion

# Adding a function's parameters to its symbol table
def p_np_function_parameters(p):
    'np_function_parameters :'
    vars_table.add_function_parameters(p[-1])
        
# Adding a variable to the symbols table
def p_np_add_variable(p):
    'np_add_variable :'
    vars_table.add_variable(p)

def p_np_end_global_scope(p):
    'np_end_global_scope :'
    vars_table.global_scope = False
    
def p_np_add_operator(p):
    'np_add_operator :'
    stack_operators.append(p[-1])

def p_np_add_write_operator(p):
    'np_add_write_operator :'
    stack_operators.append("output")

def p_np_add_operand(p):
    'np_add_operand :'

    # Revisar si el operando existe en memoria global
    if p[-1] in vars_table.vars_table["global"]["vars"]:
        memory_pos = vars_table.vars_table["global"]["vars"][p[-1]]["memory_position"]
        stack_operands.append(memory_pos)
        stack_types.append(vars_table.vars_table["global"]["vars"][p[-1]]["type"])
    # Revisar si el operando existe en memoria local
    elif p[-1] in vars_table.vars_table[vars_table.current_function]["vars"]:
        memory_pos = vars_table.vars_table[vars_table.current_function]["vars"][p[-1]]["memory_position"]
        stack_operands.append(memory_pos)
        stack_types.append(vars_table.vars_table[vars_table.current_function]["vars"][p[-1]]["type"])
    # Mostrar error cuando el operando no existe
    else:
        raise VarsTableException(f"The variable \'{p[-1]}\' does not exist")

def p_np_add_int(p):
    'np_add_int :'
    
    if p[-1] not in vars_table.constants_table['int']:
        memory_pos = memory.malloc(1,'constant', 'int')
        vars_table.constants_table['int'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['int'][p[-1]]['memory_position'])
    stack_types.append('int')

def p_np_add_float(p):
    'np_add_float :'
    
    if p[-1] not in vars_table.constants_table['float']:
        memory_pos = memory.malloc(1,'constant', 'float')
        vars_table.constants_table['float'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['float'][p[-1]]['memory_position'])
    stack_types.append('float')
    
def p_np_add_string(p):
    'np_add_string :'
    
    if p[-1] not in vars_table.constants_table['string']:
        memory_pos = memory.malloc(1,'constant', 'string')
        vars_table.constants_table['string'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['string'][p[-1]]['memory_position'])
    stack_types.append('string')
    
def p_np_add_bool(p):
    'np_add_bool :'
    
    if p[-1] not in vars_table.constants_table['bool']:
        memory_pos = memory.malloc(1,'constant', 'bool')
        vars_table.constants_table['bool'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['bool'][p[-1]]['memory_position'])
    stack_types.append('bool')
    
    
def p_np_add_plusminus(p):
    'np_add_plusminus :'
    
    
    if stack_operators and (stack_operators[-1] == '+' or stack_operators[-1] == "-"):
        operator = stack_operators.pop()
        
        right_operand = stack_operands.pop()
        right_type = stack_types.pop()
        
        left_operand = stack_operands.pop()
        left_type = stack_types.pop()

        result = None
        result_type = semantic_cube[left_type][right_type][operator]

        if result_type != 'error':
            if not vars_table.global_scope:
                result = memory.malloc(1, "local_temp", result_type)
            # Generate Quad
            quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            stack_operands.append(result)
            stack_types.append(result_type)
        else:
            raise TypeError("Type Mismatch")

def p_np_add_multiplydivision(p):
    'np_add_multiplydivision :'

    if stack_operators and (stack_operators[-1] == '*' or stack_operators[-1] == "/"):
        operator = stack_operators.pop()
        
        right_operand = stack_operands.pop()
        right_type = stack_types.pop()
        
        left_operand = stack_operands.pop()
        left_type = stack_types.pop()

        result = None
        result_type = semantic_cube[left_type][right_type][operator]

        if result_type != 'error':
            if not vars_table.global_scope:
                result = memory.malloc(1, "local_temp", result_type)
            # Generate Quad
            quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            stack_operands.append(result)
            stack_types.append(result_type)
        else:
            raise TypeError("Type Mismatch")
        
def p_np_add_conditionals(p):
    'np_add_conditionals :'

    if stack_operators and (stack_operators[-1] == '==' or stack_operators[-1] == "!=" or stack_operators[-1] == ">" or stack_operators[-1] == "=>" or stack_operators[-1] == "<" or stack_operators[-1] == "=<"):
        operator = stack_operators.pop()
        
        right_operand = stack_operands.pop()
        right_type = stack_types.pop()
        
        left_operand = stack_operands.pop()
        left_type = stack_types.pop()

        result = None
        result_type = semantic_cube[left_type][right_type][operator]

        if result_type != 'error':
            if not vars_table.global_scope:
                result = memory.malloc(1, "local_temp", result_type)
            # Generate Quad
            quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            stack_operands.append(result)
            stack_types.append(result_type)
        else:
            raise TypeError("Type Mismatch")

def p_np_add_and(p):
    'np_add_and :'

    if stack_operators and (stack_operators[-1] == "&&"):
        operator = stack_operators.pop()
        
        right_operand = stack_operands.pop()
        right_type = stack_types.pop()
        
        left_operand = stack_operands.pop()
        left_type = stack_types.pop()

        result = None
        result_type = semantic_cube[left_type][right_type][operator]

        if result_type != 'error':
            if not vars_table.global_scope:
                result = memory.malloc(1, "local_temp", result_type)
            # Generate Quad
            quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            stack_operands.append(result)
            stack_types.append(result_type)
        else:
            raise TypeError("Type Mismatch")

def p_np_add_or(p):
    'np_add_or :'

    if stack_operators and (stack_operators[-1] == "||"):
        operator = stack_operators.pop()
        
        right_operand = stack_operands.pop()
        right_type = stack_types.pop()
        
        left_operand = stack_operands.pop()
        left_type = stack_types.pop()

        result = None
        result_type = semantic_cube[left_type][right_type][operator]

        if result_type != 'error':
            if not vars_table.global_scope:
                result = memory.malloc(1, "local_temp", result_type)
            # Generate Quad
            quad_list.append(Quadruple(operator, left_operand, right_operand, result))
            stack_operands.append(result)
            stack_types.append(result_type)
        else:
            raise TypeError("Type Mismatch")
        
yacc.yacc()

def run():
    if len(sys.argv) == 2:
        program_file = sys.argv[1]

        with open(sys.argv[1], 'r') as f:
            data = f.read()
            yacc.parse(data)
            
            # Used for debugging
            print("Printing from parserv2.py for debugging")
            pprint(vars_table.vars_table)
            pprint(vars_table.constants_table)
            temp = vars_table.constants_table
            
            with open('output.sgo', 'w') as fp:
                for q in quad_list:
                    fp.write(f"{q}\n")
            print("Parser finished reading the file.")
            print("Finished printing from parserv2.py")
            print("---------------------------------")
            
            return [vars_table.constants_table,vars_table.vars_table]
    
    
if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        program_file = sys.argv[1]

        with open(sys.argv[1], 'r') as f:
            data = f.read()
            yacc.parse(data)
            
            # Used for debugging
            print("Print from parserv2 for debugging")
            pprint(vars_table.vars_table)
            pprint(vars_table.constants_table)
            temp = vars_table.constants_table
            
            with open('output.sgo', 'w') as fp:
                for q in quad_list:
                    fp.write(f"{q}\n")
            print("Parser finished reading the file.")
            print("Finished printing from parserv2")
            print("---------------------------------")
            
