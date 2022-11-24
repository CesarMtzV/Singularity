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
debug_mode = False

num_temps = {'int': 0, 'float': 0, 'bool': 0, 'string': 0, 'pointer': 0} # Local Temps Table

## Se guardan los operadoes como + - * / y los GOTOS GOTOF GOTOV
stack_operators = []
stack_operands = []
stack_types = []
stack_jumps = []
stack_dimensions = []

quad_list = []

# Variables Auxiliares
is_void_function = False
has_return_stmt = False
ip_counter = 0
param_counter = 0 # Número de parámetros que se mandan a la hora de llamar una funcion 
called_function = None

# Variables para calculos de arreglos
current_var = None
current_array_var = None
stack_current_var = []
is_array = False
is_matrix = False
R = 1

# Variables auxiliares para clases
temp_constructor_signature = []
is_void_method = False
is_class = False

################
### PROGRAMA ###
################
def p_programa(t):
    '''
    programa    : np_goto_main programa_1 cuerpo
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
    cuerpo      :  np_end_global_scope cuerpo_2 cuerpo_1 funcion_main
    '''
    global ip_counter

    # Generar Quad del fin de programa
    quad_list.append(Quadruple(ip_counter, "END", None, None, None))
    ip_counter += 1

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
    vars_1      : SEMICOLON np_assign_normal_var_memory vars_4
                | vars_2
    '''

def p_vars_2(t):
    '''
    vars_2      : LBRACKET np_is_array VAR_CONST_INT np_calculate_r RBRACKET vars_3
    '''

def p_vars_3(t):
    '''
    vars_3      : LBRACKET np_is_matrix VAR_CONST_INT np_calculate_r RBRACKET SEMICOLON np_end_matrix vars_4 
                | SEMICOLON np_end_array vars_4
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
    funcion_main : MAIN np_start_main LPAREN RPAREN LCURLY bloque RCURLY
    '''
    # np_start_main : guardar el número de cuadruplo para el GOTO y agregar el main como una función VOID

def p_funciones(t):
    '''
    funciones   : funcion funciones
                | epsilon
    '''

# TODO: Agregar NPs y funcionalidad a funciones tipo
def p_function(t):
    '''
    funcion     : FUNCTION VOID ID np_add_void_function LPAREN params RPAREN LCURLY vars_sup np_set_function_quad bloque RCURLY np_end_function
                | FUNCTION tipo_simple np_reset_is_void ID np_add_function LPAREN params RPAREN LCURLY vars_sup np_set_function_quad bloque RCURLY np_check_return np_end_function
                | epsilon
    '''
    # np_set_function_quad : Guardar en la tabla de variables el quadruplo de inicio de la función


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
                | llamada SEMICOLON
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
    asigna      : variable ASSIGN np_add_operator exp SEMICOLON
    '''
    global ip_counter
    
    operator = stack_operators.pop()
    operand = stack_operands.pop()
    result = stack_operands.pop()

    quad_list.append(Quadruple(ip_counter, operator, operand, None, result))
    ip_counter += 1


def p_llamada(t):
    '''
    llamada     : EXECUTE ID np_check_function_name LPAREN llamada_1 np_check_last_param RPAREN
    '''
    # np_check_function_name : Revisar que la funcion existe en el directorio de funciones
    # np_check_last_param : Revisar coherencia con el número de parámetros enviados
    global ip_counter, param_counter

    # Generar código de operación GOSUB
    quad_list.append(Quadruple(ip_counter, "GOSUB", called_function, None, None))
    ip_counter += 1

    # Parche guadalupano
    if called_function in vars_table.vars_table["global"]["vars"]:
        function_type = vars_table.vars_table["global"]["vars"][called_function]["type"]
        function_result = memory.malloc(1, "local_temp", function_type)

        quad_list.append(Quadruple(ip_counter, "=", vars_table.vars_table["global"]["vars"][called_function]["memory_position"], None, function_result))
        ip_counter += 1

        stack_operands.append(function_result)
        stack_types.append(function_type)

        # Sumar al número de variables en función
        vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][function_type] += 1

    # Reiniciar el contador de parámetros
    param_counter = 0

def p_llamada_1(t):
    '''
    llamada_1   : llamada_2
                | epsilon
    '''

def p_llamada_2(t):
    '''
    llamada_2   : exp np_check_param np_increase_param_counter llamada_3
    '''
    # np_check_param : Revisar si el tipo de parámetro enviado concuerda con la Function Signature
    # np_increase_param_counter : Aumentar el contador de parámetros

def p_llamada_3(t):
    '''
    llamada_3   : COMMA llamada_2
                | epsilon
    '''

def p_lectura(t):
    '''
    lectura : INPUT np_add_operator CIN variable SEMICOLON
    '''
    global ip_counter

    operator = stack_operators.pop()
    operand = stack_operands.pop()

    quad_list.append(Quadruple(ip_counter, operator, None, None, operand))
    ip_counter += 1

def p_escritura(t):
    '''
    escritura : OUTPUT escritura_1 SEMICOLON
    '''
    

def p_escritura_1(t):
    '''
    escritura_1 : COUT np_add_write_operator escritura_2 np_generate_write_quad escritura_3
    '''

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
    condicion : IF LPAREN exp RPAREN np_condicion_gotof LCURLY bloque RCURLY condicion_1
    '''

def p_condicion_1(t):
    '''
    condicion_1 : ELSE np_goto_else LCURLY bloque RCURLY np_end_condition
                | epsilon np_end_condition
    '''

def p_ciclo_w(t):
    '''
    ciclo_w : WHILE np_while_1 LPAREN exp RPAREN np_while_2 LCURLY bloque RCURLY np_while_3
    '''

def p_ciclo_f(t):
    '''
    ciclo_f : FOR LPAREN ID np_for_check_id IN RANGE LPAREN VAR_CONST_INT np_add_int np_for_1 COMMA VAR_CONST_INT np_add_int np_for_2 RPAREN RPAREN LCURLY bloque RCURLY np_for_end
    '''

def p_return(t):
    '''
    return  : RETURN np_add_operator exp SEMICOLON
    '''
    global ip_counter, has_return_stmt

    if is_void_function:
        raise VarsTableException(f"Function '{vars_table.current_function}' is of type void. RETURN statement is not allowed")
    
    has_return_stmt = True

    operator = stack_operators.pop()
    operand = stack_operands.pop()
    stack_types.pop()

    quad_list.append(Quadruple(ip_counter, operator, None, None, operand))
    ip_counter += 1

##############
### CLASES ###
##############

def p_clase(t):
    '''
    clase       : CLASS ID np_add_class LCURLY ATTRIBUTES COLON attrs constructor metodos RCURLY clase
                | CLASS ID INHERITS ID LCURLY ATTRIBUTES COLON attrs constructor metodos RCURLY clase
                | epsilon
    '''

def p_constructor(t):
    '''
    constructor : CONSTRUCTOR COLON ID np_check_class_name LPAREN constructor_params np_check_constructor_signature RPAREN SEMICOLON
    '''
    # np_check_class_name : Revisa que el constructor tenga el mismo nombre que la clase
    # np_check_constructor_signature : Revisa que los parametros tengan el mismo orden que la firma del constructor

def p_constructor_params(t):
    '''
    constructor_params  : tipo_simple np_add_constructor_param constructor_params_1
                        | epsilon
    '''
    # np_add_constructor_param : Agrega el tipo a una lista temporal para despues validarlo con la firma correcta del constructor

def p_constructor_params_1(t):
    '''
    constructor_params_1    : COMMA constructor_params
                            | epsilon
    '''

def p_attrs(t):
    '''
    attrs           : tipo_simple ID np_add_attribute SEMICOLON attrs
                    | epsilon
    '''

def p_metodos(t):
    '''
    metodos     : METHODS COLON metodo
    '''

def p_metodo(t):
    '''
    metodo      : METHOD VOID ID np_add_void_method LPAREN metodo_params RPAREN LCURLY np_set_method_start_quad bloque RCURLY np_end_method metodo
                | METHOD tipo_simple ID np_add_method LPAREN metodo_params RPAREN LCURLY np_set_method_start_quad bloque RCURLY np_end_method metodo
                | epsilon
    '''
    # np_set_method_start_quad : Guardar el cuádruplo de inicio del método

def p_metodo_params(t):
    '''
    metodo_params   : tipo_simple ID np_add_method_param metodo_params_1
                    | epsilon
    '''
    # np_add_method_param : Agregar el parámetro a su método correspondiente y agregar su tipo a la Method Signature

def p_metodo_params_1(t):
    '''
    metodo_params_1     : COMMA metodo_params
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
    factor_1    : LPAREN np_add_fondo_falso exp RPAREN np_remove_fondo_falso
                    | epsilon
    '''
    # np_add_fondo_falso : agregar un '(' a la pila de operadores
    # np_remove_fondo_falso : quitar el '(' de la pila de operadores

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
    factor_3    : llamada
                | epsilon
    '''

def p_factor_4(t):
    '''
    factor_4    : variable
                | epsilon
    '''

# REGLAS DE VARIABLE
def p_variable(t):
    '''
    variable    : ID np_add_operand variable_1
    '''

def p_variable_1(t):
    '''
    variable_1  : LBRACKET np_verify_if_array exp np_verify_range RBRACKET variable_2
                | epsilon
    '''

def p_variable_2(t):
    '''
    variable_2  : LBRACKET np_verify_if_matrix exp np_verify_range_matrix RBRACKET
                | epsilon np_verify_if_array_2
    '''

def p_epsilon(t):
    'epsilon : '
    pass

def p_error(t):
    if not t:
        raise ParserException("Syntax error: Unexpected END OF FILE")
    else:
        raise ParserException(f"Syntax error: Unexpected {t.type}({t.value}) on line {t.lineno} ")


##########################
### PUNTOS NEURALGICOS ###
##########################

# Adding a function to the functions directory
def p_np_add_function(p):
    'np_add_function :'
    global is_class

    is_class = False
    vars_table.add_function(p[-1], False) # p[-1] = nombre_funcion
    pass

def p_np_add_void_function(p):
    'np_add_void_function :'
    global is_void_function, is_class
    
    is_class = False
    vars_table.add_function(p[-1], True) # p[-1] = nombre_funcion
    is_void_function = True
    

# Adding a function's parameters to its symbol table
def p_np_function_parameters(p):
    'np_function_parameters :'
    vars_table.add_function_parameters(p[-1])
        
# Adding a variable to the symbols table
def p_np_add_variable(p):
    'np_add_variable :'
    global current_var, R
    current_var = p[-1]
    R = 1
    vars_table.add_variable(p)

# Agregar memoria a una variable con 0 dimensiones
def p_np_assign_normal_var_memory(p):
    'np_assign_normal_var_memory :'
    global current_var
    # Variable normal
    vars_table.assign_memory(current_var, 1, 0)

# Agregar una dimensión a la variable actual
def p_np_is_array(p):
    'np_is_array :'
    global current_var
    
    vars_table.add_dimensions(current_var)

    # Agregar el número 0 a la tabla de constantes
    if 0 not in vars_table.constants_table["int"]:
        vars_table.constants_table["int"][0] = {
            "memory_position" : memory.malloc(1, "constant", "int")
        }

# Realizar el cálculo de la R para calculos con arreglos
def p_np_calculate_r(p):
    'np_calculate_r :'
    global R, current_var

    # Guardar el límite en la tabla de constantes
    limit = p[-1]
    if limit not in vars_table.constants_table["int"]:
        vars_table.constants_table["int"][limit] = {
            "memory_position" : memory.malloc(1, "constant", "int")
        }

    # Guardar el límite en la tabla de variables
    scope = vars_table.exists(current_var)
    dim = vars_table.vars_table[scope]["vars"][current_var]["dimensions"]
    if dim == 1:
        vars_table.vars_table[scope]["vars"][current_var]["limit_1"] = limit - 1
        
        # Guardar el límite en tabla de constantes
        if limit - 1 not in vars_table.constants_table["int"]:
            vars_table.constants_table["int"][limit - 1] = {
                "memory_position" : memory.malloc(1, "constant", "int")
            }
    elif dim == 2:
        vars_table.vars_table[scope]["vars"][current_var]["limit_2"] = limit - 1
        
        # Guardar el límite en tabla de constantes
        if limit - 1 not in vars_table.constants_table["int"]:
            vars_table.constants_table["int"][limit - 1] = {
                "memory_position" : memory.malloc(1, "constant", "int")
            }
    
    # Los arreglos comienzan en 0, por lo que omitimos la resta del límite inferior
    R = R * (limit)

# Asignarle la memoria a un arreglo
def p_np_end_array(p):
    'np_end_array :'
    global current_var

    # Generar la memoria para el arreglo
    vars_table.assign_memory(current_var, R, 0)

# Agregarle una dimensión a la variable actual
def p_np_is_matrix(p):
    'np_is_matrix :'
    global current_var

    vars_table.add_dimensions(current_var)

# Asignarle memoria de matriz a la variable actual
def p_np_end_matrix(p):
    'np_end_matrix :'
    
    vars_table.assign_memory(current_var, R, 0)

# Revisar si la variable es un arreglo
def p_np_verify_if_array(p):
    'np_verify_if_array :'
    global current_var, current_array_var
    stack_operands.pop()
    stack_types.pop()

    current_array_var = stack_current_var[-1]

    # Verificar que la var no sea una variable simple
    scope = vars_table.exists(current_var)
    dim = vars_table.vars_table[scope]["vars"][current_var]["dimensions"]
    if dim == 0:
        raise VarsTableException(f"Variable '{current_var}' is not an array")
    
    stack_operators.append("(")

# Revisar si la variable es un arreglo (en caso de querer accesarla como una matriz)
def p_np_verify_if_array_2(p):
    'np_verify_if_array_2 :'
    global current_var, current_array_var

    # Verificar que la var tenga 1 dimensión
    scope = vars_table.exists(current_var)
    dim = vars_table.vars_table[scope]["vars"][current_var]["dimensions"]
    if dim == 2:
        raise VarsTableException(f"Variable '{current_var}' is not an array")
    
    if stack_current_var:
        stack_current_var.pop()
        stack_operators.pop()

# Revisar si la variable es una matriz
def p_np_verify_if_matrix(p):
    'np_verify_if_matrix :'
    global current_array_var

    scope = vars_table.exists(current_var)
    dim = vars_table.vars_table[scope]["vars"][current_array_var]["dimensions"]
    if dim == 0 or dim == 1:
        raise VarsTableException(f"Variable '{current_array_var}' is not a matrix")

# Creación de cuádruplos para verifica el rango de indexación en arreglos y matrices
def p_np_verify_range(p):
    'np_verify_range :'
    global ip_counter, current_array_var

    scope = vars_table.exists(current_var)
    dim = vars_table.vars_table[scope]["vars"][current_array_var]["dimensions"]
    
    if dim == 1:
        limit = vars_table.vars_table[scope]["vars"][current_array_var]["limit_1"]
        # Obtener memoria de los límites
        low_limit = vars_table.constants_table["int"][0]["memory_position"]
        up_limit = vars_table.constants_table["int"][limit]["memory_position"]

        # Generar cuádruplo de verificación
        quad_list.append(Quadruple(ip_counter, "VER", stack_operands[-1], low_limit, up_limit))
        ip_counter += 1

        # Sumarle al límite la dirección base
        temp_pointer = memory.malloc(1, "local_temp", "pointer")
        vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["pointer"] += 1
        
        current_var_memory = vars_table.vars_table[scope]["vars"][current_array_var]["memory_position"]
        
        if current_var_memory not in vars_table.constants_table['int']:
            vars_table.constants_table['int'][current_var_memory] = {'memory_position' : memory.malloc(1,'constant','int')}
            
        current_operand = stack_operands.pop()
        stack_types.pop()
        
        quad_list.append(Quadruple(ip_counter, "+", current_operand, vars_table.constants_table['int'][current_var_memory]['memory_position'], temp_pointer))
        ip_counter += 1

        stack_operands.append(f'({temp_pointer})')
        stack_types.append("pointer")
    elif dim == 2: 
        limit = vars_table.vars_table[scope]["vars"][current_array_var]["limit_1"]
        up_limit = vars_table.constants_table["int"][limit]["memory_position"]
        
        limit_2 = vars_table.vars_table[scope]["vars"][current_array_var]["limit_2"]
        
        low_limit = vars_table.constants_table["int"][0]["memory_position"]

        # Crear cuádruplo de VER para la primer dimensión
        quad_list.append(Quadruple(ip_counter, "VER", stack_operands[-1], low_limit, up_limit))
        ip_counter += 1

        operand = stack_operands.pop()
        stack_types.pop()

        m1 = int(((limit + 1) * (limit_2 + 1)) / (limit + 1))
        
        if m1 not in vars_table.constants_table["int"]:
            vars_table.constants_table["int"][m1] = {
                "memory_position" : memory.malloc(1, "constant", "int")
            }
        m1_memory = vars_table.constants_table["int"][m1]["memory_position"]
        
        temp_1 = memory.malloc(1, "local_temp", "int")
        vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["int"] += 1

        quad_list.append(Quadruple(ip_counter, "*", operand, m1_memory, temp_1))
        ip_counter += 1

        stack_operands.append(temp_1)
        stack_types.append("int")
        
# Verificar el rango del segundo índice de una matriz
def p_np_verify_range_matrix(p):
    'np_verify_range_matrix :'
    global ip_counter, current_var

    scope = vars_table.exists(current_var)
    
    limit_2 = vars_table.vars_table[scope]["vars"][current_array_var]["limit_2"]
    limit_2_memory = vars_table.constants_table["int"][limit_2]["memory_position"]

    low_limit = vars_table.constants_table["int"][0]["memory_position"]

    operand_2 = stack_operands.pop()
    stack_types.pop()

    # temp_1 = memory.malloc(1, "local_temp", "int")
    temp_2 = memory.malloc(1, "local_temp", "int")
    pointer = memory.malloc(1, "local_temp", "pointer")
    
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["pointer"] += 1
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["int"] += 1

    # Verificar el segúndo límite
    quad_list.append(Quadruple(ip_counter, "VER", operand_2, low_limit, limit_2_memory))
    ip_counter += 1

    # s1*m1 + s2
    temp_1 = stack_operands.pop()
    stack_types.pop()
    quad_list.append(Quadruple(ip_counter, "+", temp_1, operand_2, temp_2))
    ip_counter += 1

    # Sumar dirección base de variable
    current_var_memory = vars_table.vars_table[scope]["vars"][current_var]["memory_position"]
    
    if current_var_memory not in vars_table.constants_table['int']:
        vars_table.constants_table['int'][current_var_memory] = {'memory_position' : memory.malloc(1,'constant','int')}
        
    quad_list.append(Quadruple(ip_counter, "+", temp_2, vars_table.constants_table['int'][current_var_memory]['memory_position'], pointer))
    ip_counter += 1
    
    stack_operands.append(f'({pointer})')
    stack_types.append("pointer")
    stack_operators.pop()
    if debug_mode:
        quad_list.append(f"Finished RANGE MATRIX for {current_var}\n")

# Marcar el final del scope global
def p_np_end_global_scope(p):
    'np_end_global_scope :'
    vars_table.global_scope = False

# Agregar un operador al stack de operadores
def p_np_add_operator(p):
    'np_add_operator :'
    stack_operators.append(p[-1])

# Agregar el operador de escritura al stack de operadores
def p_np_add_write_operator(p):
    'np_add_write_operator :'
    stack_operators.append("output")

# Agregar un operando al stack de operandos
def p_np_add_operand(p):
    'np_add_operand :'
    global current_var, stack_current_var

    current_operand = p[-1]

    # Revisar si el operando existe en memoria global
    if current_operand in vars_table.vars_table["global"]["vars"]:
        memory_pos = vars_table.vars_table["global"]["vars"][current_operand]["memory_position"]
        stack_operands.append(memory_pos)
        stack_types.append(vars_table.vars_table["global"]["vars"][p[-1]]["type"])
        if vars_table.vars_table["global"]["vars"][p[-1]]["dimensions"] and vars_table.vars_table["global"]["vars"][p[-1]]["dimensions"] > 0:
            stack_current_var.append(p[-1])
        current_var = p[-1]
    # Revisar si el operando existe en memoria local
    elif vars_table.current_function != "" and current_operand in vars_table.vars_table[vars_table.current_function]["vars"]:
        memory_pos = vars_table.vars_table[vars_table.current_function]["vars"][current_operand]["memory_position"]
        stack_operands.append(memory_pos)
        stack_types.append(vars_table.vars_table[vars_table.current_function]["vars"][p[-1]]["type"])
        if vars_table.vars_table[vars_table.current_function]["vars"][p[-1]]["dimensions"] and vars_table.vars_table[vars_table.current_function]["vars"][p[-1]]["dimensions"] > 0:
            stack_current_var.append(p[-1])
        current_var = p[-1]
    elif current_operand in vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["vars"]:
        memory_pos = vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["vars"][current_operand]["memory_position"]
        stack_operands.append(memory_pos)
        stack_types.append(vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["vars"][current_operand]["type"])
        current_var = current_operand
    # Mostrar error cuando el operando no existe
    else:
        raise VarsTableException(f"The variable \'{p[-1]}\' does not exist")

# Agregar un entero a la tabla de constantes
def p_np_add_int(p):
    'np_add_int :'
    
    if p[-1] not in vars_table.constants_table['int']:
        memory_pos = memory.malloc(1,'constant', 'int')
        vars_table.constants_table['int'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['int'][p[-1]]['memory_position'])
    stack_types.append('int')

# Agregar un flotante a la tabla de constantes
def p_np_add_float(p):
    'np_add_float :'
    
    if p[-1] not in vars_table.constants_table['float']:
        memory_pos = memory.malloc(1,'constant', 'float')
        vars_table.constants_table['float'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['float'][p[-1]]['memory_position'])
    stack_types.append('float')

# Agregar un string a la tabla de constantes
def p_np_add_string(p):
    'np_add_string :'
    
    if p[-1] not in vars_table.constants_table['string']:
        memory_pos = memory.malloc(1,'constant', 'string')
        vars_table.constants_table['string'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['string'][p[-1]]['memory_position'])
    stack_types.append('string')

# Agregar un bool a la tabla de constantes
def p_np_add_bool(p):
    'np_add_bool :'
    
    if p[-1] not in vars_table.constants_table['bool']:
        memory_pos = memory.malloc(1,'constant', 'bool')
        vars_table.constants_table['bool'][p[-1]] = {
            'memory_position': memory_pos
        }

    stack_operands.append(vars_table.constants_table['bool'][p[-1]]['memory_position'])
    stack_types.append('bool')
    
# Verificar si existe una suma o resta pendiente para crear el cuádruplo
def p_np_add_plusminus(p):
    'np_add_plusminus :'
    global ip_counter
    
    if stack_operators and (stack_operators[-1] == '+' or stack_operators[-1] == '-'):
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

                if is_class:
                    # Sumar contador de variable local en el método de la clase
                    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["size"]["vars_temp"][result_type] += 1    
                else:
                    # Sumar contador de variable local en la función
                    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][result_type] += 1

            # Generate Quad
            quad_list.append(Quadruple(ip_counter, operator, left_operand, right_operand, result))
            ip_counter += 1
            stack_operands.append(result)
            stack_types.append(result_type)
            num_temps[result_type] +=1
        else:
            raise TypeError("Type Mismatch")

# Verificar si existe una multiplicación o división pendiente para crear el cuádruplo
def p_np_add_multiplydivision(p):
    'np_add_multiplydivision :'
    global ip_counter

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

                if is_class:
                    # Sumar contador de variable local en el método de la clase
                    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["size"]["vars_temp"][result_type] += 1    
                else:
                    # Sumar contador de variable local en la función
                    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][result_type] += 1

            # Generate Quad
            quad_list.append(Quadruple(ip_counter, operator, left_operand, right_operand, result))
            ip_counter += 1
            stack_operands.append(result)
            stack_types.append(result_type)
            num_temps[result_type] +=1
        else:
            raise TypeError("Type Mismatch")

# Verificar si existe un operador condicional pendiente para crear el cuádruplo
def p_np_add_conditionals(p):
    'np_add_conditionals :'
    global ip_counter

    if stack_operators and (stack_operators[-1] == '==' or stack_operators[-1] == "!=" or stack_operators[-1] == ">" or stack_operators[-1] == ">=" or stack_operators[-1] == "<" or stack_operators[-1] == "<="):
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

                if is_class:
                    # Sumar contador de variable local en el método de la clase
                    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["size"]["vars_temp"][result_type] += 1    
                else:
                    # Sumar contador de variable local en la función
                    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][result_type] += 1

            # Generate Quad
            quad_list.append(Quadruple(ip_counter, operator, left_operand, right_operand, result))
            ip_counter += 1
            stack_operands.append(result)
            stack_types.append(result_type)
            num_temps[result_type] +=1
        else:
            raise TypeError("Type Mismatch")

# Verificar si existe un operador AND pendiente para crear el cuádruplo
def p_np_add_and(p):
    'np_add_and :'
    global ip_counter

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

                if is_class:
                    # Sumar contador de variable local en el método de la clase
                    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["size"]["vars_temp"][result_type] += 1    
                else:
                    # Sumar contador de variable local en la función
                    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][result_type] += 1

            # Generate Quad
            quad_list.append(Quadruple(ip_counter, operator, left_operand, right_operand, result))
            ip_counter += 1
            stack_operands.append(result)
            stack_types.append(result_type)
            num_temps[result_type] +=1
        else:
            raise TypeError("Type Mismatch")

# Verificar si existe un operador OR pendiente para crear el cuádruplo
def p_np_add_or(p):
    'np_add_or :'
    global ip_counter

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

                if is_class:
                    # Sumar contador de variable local en el método de la clase
                    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["size"]["vars_temp"][result_type] += 1    
                else:
                    # Sumar contador de variable local en la función
                    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"][result_type] += 1

            # Generate Quad
            quad_list.append(Quadruple(ip_counter, operator, left_operand, right_operand, result))
            ip_counter += 1
            stack_operands.append(result)
            stack_types.append(result_type)
            num_temps[result_type] +=1
        else:
            raise TypeError("Type Mismatch")

# Agregar un fondo falso al stack de operadores
def p_np_add_fondo_falso(p):
    'np_add_fondo_falso :'

    stack_operators.append("(")

# Remover el fondo falso del stack de operadores
def p_np_remove_fondo_falso(p):
    'np_remove_fondo_falso :'

    stack_operators.pop()

# Generar el cuádruplo de escritura
def p_np_generate_write_quad(p):
    'np_generate_write_quad :'
    global ip_counter

    operator = stack_operators.pop()
    operand = stack_operands.pop()

    quad_list.append(Quadruple(ip_counter, operator, None, None, operand))
    ip_counter += 1

# Crear el cuádruplo de código de operación GOTOF
def p_np_condicion_gotof(p):
    'np_condicion_gotof :'
    global ip_counter

    exp_type = stack_types.pop()
    if exp_type != 'bool':
        raise TypeError(f"Type Mismatch in the IF condition. Expected 'bool' but received '{exp_type}'")
    else:
        result = stack_operands.pop()
        # Generar el GOTOF con el salto pendiente
        quad_list.append(Quadruple(ip_counter, "GOTOF", result, None, None))
        ip_counter += 1

        stack_jumps.append(ip_counter - 1)

# Crear el cuádruplo de código de operación GOTO en la condición ELSE
def p_np_goto_else(p):
    'np_goto_else :'
    global ip_counter

    quad_list.append(Quadruple(ip_counter, "GOTO", None, None, None))
    ip_counter += 1
    
    false = stack_jumps.pop()
    stack_jumps.append(ip_counter - 1)

    quad_list[false].result = ip_counter

# Marcar la dirección del salto pendiente
def p_np_end_condition(p):
    'np_end_condition :'
    global ip_counter

    end = stack_jumps.pop()

    quad_list[end].result = ip_counter

# Agregar al stack de salto el inicio del ciclo WHILE
def p_np_while_1(p):
    'np_while_1 :'
    global ip_counter

    stack_jumps.append(ip_counter)

# Crear el cuádruplo GOTOF si la condición del WHILE falla
def p_np_while_2(p):
    'np_while_2 :'
    global ip_counter

    exp_type = stack_types.pop()
    if exp_type != 'bool':
        raise TypeError('Type Mismatch: WHILE conditions is not BOOL')
    else:
        result = stack_operands.pop()

        quad_list.append(Quadruple(ip_counter, "GOTOF", result, None, None))
        ip_counter += 1

        stack_jumps.append(ip_counter - 1)

# Crear el GOTO al inicio del WHILE
def p_np_while_3(p):
    'np_while_3 :'
    global ip_counter

    end = stack_jumps.pop()
    return_quad = stack_jumps.pop()

    quad_list.append(Quadruple(ip_counter, "GOTO", None, None, return_quad))
    ip_counter += 1

    quad_list[end].result = ip_counter

# Revisar que la variable iterador existe y sea tipo entera. Agregar el 1 a la tabla de constantes
def p_np_for_check_id(p):
    'np_for_check_id :'
    # La variable que se usará como iterador
    var_iterator = p[-1]

    scope = vars_table.exists(var_iterator)

    if vars_table.vars_table[scope]["vars"][var_iterator]["type"] != "int":
        raise VarsTableException(f"Variable '{var_iterator}' is NOT of type INT")
    
    stack_operands.append(vars_table.vars_table[scope]["vars"][var_iterator]["memory_position"])
    stack_types.append(vars_table.vars_table[scope]["vars"][var_iterator]["type"])

    # Agregar el número 1 a la tabla de constantes para usarlo en el aumento del iterador
    if 1 not in vars_table.constants_table["int"]:
        vars_table.constants_table["int"][1] = {
            "memory_position" : memory.malloc(1, "constant", "int")
        }

# Agregar el límite inferior del for y asignar valores
def p_np_for_1(p):
    'np_for_1 :'
    global ip_counter

    # Obtener la posicion de memoria de la constante
    range_start_memory = vars_table.constants_table["int"][p[-2]]["memory_position"]
    
    # Se eliminan porque el NP add_int agrega los enteros a las pilas, pero en este caso no los ocupamos
    stack_operands.pop()
    stack_types.pop()
    
    # Variable entera declarada como iterador
    iterator = stack_operands[-1]
    
    # Variable de control temporal
    control_temp = memory.malloc(1, "local_temp", "int")
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["int"] += 1

    stack_operands.append(control_temp)
    stack_types.append("int")

    # Asignar el valor del inicio del FOR a la variable iterador
    quad_list.append(Quadruple(ip_counter, "=", range_start_memory, None, iterator))
    ip_counter += 1
    
    # Asignar el valor del iterador a la variable temporal
    quad_list.append(Quadruple(ip_counter, "=", iterator, None, control_temp))
    ip_counter += 1
    
    num_temps['int'] += 1

# Agregar el límite superior del for y asignar valores
def p_np_for_2(p):
    'np_for_2 :'
    global ip_counter

    range_end_memory = vars_table.constants_table["int"][p[-2]]["memory_position"]
    
    control_temp = memory.malloc(1, "local_temp", "int")
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["int"] += 1
    
    condition_temp = memory.malloc(1, "local_temp", "bool")
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["bool"] += 1

    # Se eliminan porque el NP add_int agrega los enteros a las pilas, pero en este caso no los ocupamos
    stack_operands.pop()
    stack_types.pop()

    prev_control = stack_operands[-1]

    quad_list.append(Quadruple(ip_counter, "=", range_end_memory, None, control_temp))
    ip_counter += 1
    
    quad_list.append(Quadruple(ip_counter, "<=", prev_control, control_temp, condition_temp))
    ip_counter += 1
    stack_jumps.append(ip_counter - 1)
    
    quad_list.append(Quadruple(ip_counter, "GOTOF", condition_temp, None, None))
    ip_counter += 1
    stack_jumps.append(ip_counter - 1)
    
    num_temps['int'] += 1
    num_temps['bool'] += 1
    
# Sumar 1 a la variable de control y regresar a la condición del FOR
def p_np_for_end(p):
    'np_for_end :'
    global ip_counter

    # Variables
    prev_control = stack_operands.pop()
    iterator = stack_operands.pop()
    temp = memory.malloc(1, "local_temp", "int")
    vars_table.vars_table[vars_table.current_function]["size"]["vars_temp"]["int"] += 1
    
    # Limpiar stack de tipos
    stack_types.pop()
    stack_types.pop()

    step = vars_table.constants_table["int"][1]["memory_position"]
    
    # Sumarle 1 a la variable de control
    quad_list.append(Quadruple(ip_counter, "+", step, prev_control, temp))
    ip_counter += 1
    
    # Asignarle el valor de temp a la variable de control
    quad_list.append(Quadruple(ip_counter, "=", temp, None, prev_control))
    ip_counter += 1

    # Asignarle el valor de variable de control al iterador
    quad_list.append(Quadruple(ip_counter, "=", prev_control, None, iterator))
    ip_counter += 1

    # GOTO para regresar a la condición del FOR
    gotof = stack_jumps.pop()
    for_condition = stack_jumps.pop()
    quad_list.append(Quadruple(ip_counter, "GOTO", None, None, for_condition))
    ip_counter += 1

    quad_list[gotof].result = ip_counter
    
    num_temps['int'] += 1

# Guardar en el directorio de funciones el cuádruplo de inicio de la función
def p_np_set_function_quad(p):
    'np_set_function_quad :'
    global ip_counter

    vars_table.vars_table[vars_table.current_function]["start_position"] = ip_counter

# Marcar la función como no VOID
def p_np_reset_is_void(p):
    'np_reset_is_void :'
    global is_void_function

    is_void_function = False

# Agregar el cuádruplo de ENDFUNC al final de la función
def p_np_end_function(p):
    'np_end_function :'
    global ip_counter, param_counter

    # TODO: Esto debe estar DESCOMENTADO en la version final. Por motivos de prueba esta comentado
    # vars_table.vars_table[vars_table.current_function].pop("vars")
    
    quad_list.append(Quadruple(ip_counter, "ENDFUNC", None, None, None))
    ip_counter += 1

    # Reiniciar la Function Signature
    vars_table.function_signature = []

# Revisar si una función tipo tiene un estatuto RETURn
def p_np_check_return(p):
    'np_check_return :'
    global has_return_stmt

    if not has_return_stmt:
        raise VarsTableException(f"Missing RETURN statement for function '{vars_table.current_function}'")

# Revisar que la función que se quiere invocar existe
def p_np_check_function_name(p):
    'np_check_function_name :'
    global ip_counter, called_function

    called_function = p[-1]

    if called_function not in vars_table.vars_table:
        raise VarsTableException(f"The function you are trying to call does not exist: '{called_function}'")
    
    # Generar el codigo de operacion ERA
    quad_list.append(Quadruple(ip_counter, "ERA", called_function, None, None))
    ip_counter += 1

    stack_operators.append("(")

# Reviar sintaxis y coherencia de argumentos de la función
def p_np_check_param(p):
    'np_check_param :'
    global param_counter, ip_counter, called_function

    if not stack_operands:
        raise VarsTableException(f"Incorrect argument syntax for function '{called_function}'")
        
    argument = stack_operands.pop()
    argument_type = stack_types.pop()

    # Revisar que el número de parámetro se encuentre dentro de las posiciones posibles de la lista
    number_of_params = len(vars_table.vars_table[called_function]['PARAMETER_TABLE'])
    if param_counter > number_of_params - 1:
        raise VarsTableException(f"Too many arguments for function '{called_function}'")

    expected_type = vars_table.vars_table[called_function]['PARAMETER_TABLE'][param_counter]

    if not argument_type == expected_type:
        raise TypeError(f"Type Mismatch: Expected '{expected_type}' but received '{argument_type}' for function '{called_function}'")
    
    # Generar código de operacion PARAMETER
    quad_list.append(Quadruple(ip_counter, "PARAMETER", argument, None, param_counter + 1))
    ip_counter += 1

    # Remover fondo falso
    stack_operators.pop()

# Incrementar el contador de parámetros
def p_np_increase_param_counter(p):
    'np_increase_param_counter :'
    global param_counter

    param_counter += 1

# Revisar el número de argumentos de la función
def p_np_check_last_param(p):
    'np_check_last_param :'
    global param_counter, called_function

    # Coherencia en el número de parámetros
    number_of_params = len(vars_table.vars_table[called_function]['PARAMETER_TABLE'])
    if param_counter > number_of_params or param_counter < number_of_params:
        raise VarsTableException(f"Incorrect number of arguments for function '{called_function}'")

# Crear el cuádruplo GOTO MAIN y guardar la posición de regreso
def p_np_goto_main(p):
    'np_goto_main :'
    global ip_counter

    # Guardar posicion del cuadruplo para regresar
    stack_jumps.append(ip_counter)

    # Generar el GOTO
    quad_list.append(Quadruple(ip_counter, "GOTO", None, None, None))
    ip_counter += 1

# Obtener la dirección de inicio del MAIN y substituirla en el primer GOTO
def p_np_start_main(p):
    'np_start_main :'
    global ip_counter
    
    memory.dealloc()

    vars_table.add_function(p[-1], True)

    return_addr = stack_jumps.pop()

    quad_list[return_addr].result = ip_counter

# Agregar una clase al directorio de funciones
def p_np_add_class(p):
    'np_add_class :'
    global is_class

    class_name = p[-1]
    is_class = True
    vars_table.add_class(class_name)

# Agregar un atributo a la clase actual
def p_np_add_attribute(p):
    'np_add_attribute :'

    attribute_name = p[-1]

    vars_table.add_attribute(attribute_name)

# Revisar que el constructor tenga el mismo nombre que la clase
def p_np_check_class_name(p):
    'np_check_class_name :'

    constructor_name = p[-1]

    if constructor_name not in vars_table.vars_table:
        raise VarsTableException(f"Constructor '{constructor_name}' must be the same as '{vars_table.current_class}'")

# Agregar un tipo del constructor a un constructor temporal
def p_np_add_constructor_param(p):
    'np_add_constructor_param :'
    global temp_constructor_signature

    temp_constructor_signature.append(vars_table.current_type)

# Revisar que el constructor tenga la misma firma declarada por el orden de los atributos
def p_np_check_constructor_signature(p):
    'np_check_constructor_signature :'

    constructor_signature = vars_table.vars_table[vars_table.current_class]["constructor"]

    if temp_constructor_signature != constructor_signature:
        raise ParserException(f"Constructor for class '{vars_table.current_class}' does not match the declared attributes. \nExpected {constructor_signature} but received {temp_constructor_signature}")

# Agregar un método void a la clase actual
def p_np_add_void_method(p):
    'np_add_void_method :'
    global is_void_method
    
    method_name = p[-1]

    vars_table.add_method(method_name, True)
    is_void_function = True

# Agregar un método con retorno a la clase actual
def p_np_add_method(p):
    'np_add_method :'
    global is_void_method

    method_name = p[-1]
    vars_table.add_method(method_name, False)
    is_void_method = False

# Agregar un parámetro al método actual
def p_np_add_method_param(p):
    'np_add_method_param :'

    vars_table.add_method_parameters(p[-1])

# Indicar el inicio del método
def p_np_set_method_start_quad(p):
    'np_set_method_start_quad :'
    global ip_counter

    vars_table.vars_table[vars_table.current_class]["methods"][vars_table.current_method]["start_position"] = ip_counter

# Crear el cuádruplo con código de operación ENDMETH
def p_np_end_method(p):
    'np_end_method :'
    global ip_counter

    # TODO: Descomentar esto en la versión final
    # vars_table.vars_table[vars_table.current_class]["methods"].pop()

    quad_list.append(Quadruple(ip_counter, "ENDMETH", None, None, None))
    ip_counter += 1

    # Reiniciar la Method Signature
    vars_table.method_signature = []

# Clase usada para errores detectados en el Parser
class ParserException(Exception):
    """Clase personalizada para los tipos de errores en el parser"""

    pass
        
yacc.yacc()

def run():
    if len(sys.argv) == 2:
        program_file = sys.argv[1]

        with open(sys.argv[1], 'r') as f:
            data = f.read()
            yacc.parse(data)
            
            # Used for debugging
            # print("Printing from parserv2.py for debugging")
            pprint(vars_table.vars_table)
            # pprint(vars_table.constants_table)
            
            with open('output.sgo', 'w') as fp:
                for q in quad_list:
                    fp.write(f"{q}\n")
            print("Parser finished reading the file.")
            print("---------------------------------")
            
            return [vars_table.constants_table,vars_table.vars_table, num_temps]
    
    
if __name__ == '__main__':
    
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        program_file = sys.argv[1]

        if len(sys.argv) == 3:
            if sys.argv[2] == "-d":
                debug_mode = True

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
            
