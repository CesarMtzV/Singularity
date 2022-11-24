from MemoryManager import MemoryManager
import parserv2
import sys

# Llamada de la clase memory manager donde están todas las listas, stacks y direcciones de memoria
memory = MemoryManager()

#Llamada de la función run del parser que regresa la tabla de constantes y la tabla de variables
tables = parserv2.run()
constants_table = tables[0]
vars_table = tables[1]

#Inicializamos stacks necesarios para la ejecución de la máquina virtual
quad_list = []
jumpStack = []
paramList = []
paramStack = []
function_name = ' '

#Comienza el ciclo que itera sobre el archivo 'output.sgo' y guarda los cuadruplos en quad_list
with open("output.sgo") as file:
    #Para cada linea del archivo .sgo
    for line in file:
        #Separamos todo por espacios y leemos la línea
        temp = line.split(' ')
        
        operator = temp[3]
        
        left = temp[5]
        if left.isdigit():
            left = int(temp[5])
            
        right = temp[7]
        if right.isdigit():
            right = int(temp[7])

        res = temp[9]
        if res.isdigit():
            res = int(temp[9])

        quad = [operator, left, right, res]
        quad_list.append(quad)

#Inicializamos la memoria constante del programa
for type in constants_table:
    for constant in constants_table[type]:
        if type == 'int':
            memory.const_ints.append(constant)
        if type == 'float':
            memory.const_floats.append(constant)
        if type == 'bool':
            memory.const_bools.append(constant)
        if type == 'string':
            memory.const_strings.append(constant)

#Inicializamos la memoria global del programa
for var in vars_table['global']['vars']:
    if vars_table['global']['vars'][var]['type'] == 'int':
        #Validamos si la variable es un arreglo
        if 'limit_1' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])+1):
                memory.global_ints.append(None)
        #Valimdamos si la variable es una matriz
        if 'limit_2' in vars_table['global']['vars'][var]:
            for i in range(0,(int(vars_table['global']['vars'][var]['limit_1'])+1)*(int(vars_table['global']['vars'][var]['limit_2'])+1)):
                memory.global_ints.append(None)
        else:
            memory.global_ints.append(None)
    if vars_table['global']['vars'][var]['type'] == 'float':
        #Validamos si la variable es un arreglo
        if 'limit_1' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])+1):
                memory.global_floats.append(None)
        #Valimdamos si la variable es una matriz
        if 'limit_2' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])*int(vars_table['global']['vars'][var]['limit_2'])+1):
                memory.global_floats.append(None)
        else:
            memory.global_floats.append(None)
    if vars_table['global']['vars'][var]['type'] == 'bool':
        memory.global_bools.append(None)
    if vars_table['global']['vars'][var]['type'] == 'string':
        memory.global_strings.append(None)

#Inicializamos la memoria temporal para el main solamente
for i in range(0, vars_table['main']['size']['vars_temp']['int']):
    memory.local_temp_ints.append(None)
for i in range(0, vars_table['main']['size']['vars_temp']['float']):
    memory.local_temp_floats.append(None)
for i in range(0, vars_table['main']['size']['vars_temp']['bool']):
    memory.local_temp_bools.append(None)
for i in range(0, vars_table['main']['size']['vars_temp']['string']):
    memory.local_temp_strings.append(None)
for i in range(0, vars_table['main']['size']['vars_temp']['pointer']):
    memory.pointers.append(None)
    
#Llamamos a las funciones reset que empujan a la pila la memoria local y temporal y la liberan para su uso más adelante
memory.resetLocalMemory();
memory.resetTempMemory();

#Función que recibe como parámetro una dirección de memoria y regresa su posicón dentro de la lista correspondiente
def getAddress(addr):
    addressToString = str(addr)
    #Revisamos si la dirección no está entre () para hacer un getAddress de un getAddress
    if addressToString[0] == '(' and addressToString[-1] == ')':
        addr = getAddress(int(addressToString[1:-1]))
    if 1000<=addr<2000:
        if memory.global_ints[addr-1000] == None:
            return
        return memory.global_ints[addr-1000]
    elif 2000<=addr<3000:
        if memory.global_temp_ints[addr-2000] == None:
            return
        return memory.global_temp_ints[addr-2000]
    elif 3000<=addr<4000:
        if memory.global_floats[addr-3000] == None:
            return
        return memory.global_floats[addr-3000]
    elif 4000<=addr<5000:
        if memory.global_temp_floats[addr-4000] == None:
            return
        return memory.global_temp_floats[addr-4000]
    elif 5000<=addr<6000:
        if memory.global_bools[addr-5000] == None:
            return
        return memory.global_bools[addr-5000]
    elif 6000<=addr<7000:
        if memory.global_temp_bools[addr-6000] == None:
            return
        return memory.global_temp_bools[addr-6000]
    elif 7000<=addr<8000:
        if memory.global_strings[addr-7000] == None:
            return
        return memory.global_strings[addr-7000]
    elif 8000<=addr<9000:
        if memory.global_temp_strings[addr-8000] == None:
            return
        return memory.global_temp_strings[addr-8000]
    elif 9000<=addr<10000:
        if memory.local_ints_stack[-1][addr-9000] == None:
            return
        return memory.local_ints_stack[-1][addr-9000]
    elif 10000<=addr<11000:
        if memory.temp_ints_stack[-1][addr-10000] == None:
            return
        return memory.temp_ints_stack[-1][addr-10000]
    elif 11000<=addr<12000:
        if memory.local_floats_stack[-1][addr-11000] == None:
            return
        return memory.local_floats_stack[-1][addr-11000]
    elif 12000<=addr<13000:
        if memory.temp_floats_stack[-1][addr-12000] == None:
            return
        return memory.temp_floats_stack[-1][addr-12000]
    elif 13000<=addr<14000:
        if memory.local_bools_stack[-1][addr-13000] == None:
            return
        return memory.local_bools_stack[-1][addr-13000]
    elif 14000<=addr<15000:
        if memory.temp_bools_stack[-1][addr-14000] == None:
            return
        return memory.temp_bools_stack[-1][addr-14000]
    elif 15000<=addr<16000:
        if memory.local_strings_stack[-1][addr-15000] == None:
            return
        return memory.local_strings_stack[-1][addr-15000]
    elif 16000<=addr<17000:
        if memory.temp_strings_stack[-1][addr-16000] == None:
            return
        return memory.temp_strings_stack[-1][addr-16000]
    elif 17000<=addr<18000:
        if memory.const_ints[addr-17000] == None:
            return
        return memory.const_ints[addr-17000]
    elif 18000<=addr<19000:
        if memory.const_floats[addr-18000] == None:
            return
        return memory.const_floats[addr-18000]
    elif 19000<=addr<20000:
        if memory.const_bools[addr-19000] == None:
            return
        return memory.const_bools[addr-19000]
    elif 20000<=addr<21000:
        if memory.const_strings[addr-20000] == None:
            return
        return memory.const_strings[addr-20000]
    elif 21000<=addr<22000:
        if memory.temp_pointers_stack[-1][addr-21000] == None:
            return
        return memory.temp_pointers_stack[-1][addr-21000]
        
#Ciclo que itera sobre cada cuadruplo dentro de quad__list
current = 0
while current < len(quad_list):
    #asignamos cada elemento de un cuadruplo a una variable temporal
    operator = quad_list[current][0]
    left = quad_list[current][1]
    right = quad_list[current][2]
    res = quad_list[current][3]
    
    #valido el operador que estoy leyendo en operator y ejecuto esa operación
    if operator == '+':
        #Revisamos los rangos de memoria y guardamos el resultado en el indice correspindiente
        if 1000<= res <2000:
            #Restar la dirección base de cada tipo de dato para accesar la posición de la lista correcta
            memory.global_ints[res-1000] = getAddress(left) + getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) + getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) + getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) + getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) + getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) + getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) + getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) + getAddress(right)
        elif 21000<= res <22000:
            memory.temp_pointers_stack[-1][res-21000] = getAddress(left) + getAddress(right)
    elif operator == '-':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) - getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) - getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) - getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) - getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) - getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) - getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) - getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) - getAddress(right)
        elif 21000<= res <22000:
            memory.temp_pointers_stack[-1][res-21000] = getAddress(left) - getAddress(right)
    elif operator == '*':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) * getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) * getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) * getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) * getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) * getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) * getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) * getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) * getAddress(right)
        elif 21000<= res <22000:
            memory.temp_pointers_stack[-1][res-21000] = getAddress(left) * getAddress(right)
    elif operator == '/':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) / getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) / getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) / getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) / getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) / getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) / getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) / getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) / getAddress(right)
        elif 21000<= res <22000:
            memory.temp_pointers_stack[-1][res-21000] = getAddress(left) / getAddress(right)
    elif operator == '>':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) > getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) > getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) > getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) > getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) > getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) > getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) > getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) > getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) > getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) > getAddress(right)
    elif operator == '<':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) < getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) < getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) < getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) < getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) < getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) < getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) < getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) < getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) < getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) < getAddress(right)
    elif operator == '>=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) >= getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) >= getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) >= getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) >= getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) >= getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) >= getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) >= getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) >= getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) >= getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) >= getAddress(right)
    elif operator == '<=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) <= getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) <= getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) <= getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) <= getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) <= getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) <= getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) <= getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) <= getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) <= getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) <= getAddress(right)
    elif operator == '==':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) == getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) == getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) == getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) == getAddress(right)
        elif 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) == getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) == getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) == getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) == getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) == getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) == getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) == getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) == getAddress(right)
    elif operator == '!=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) != getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) != getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) != getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) != getAddress(right)
        elif 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) != getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) != getAddress(right)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left) != getAddress(right)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) != getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left) != getAddress(right)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) != getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) != getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) != getAddress(right)
    elif operator == '&&':
        if 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) and getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) and getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) and getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) and getAddress(right)
    elif operator == '||':
        if 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) or getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) or getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) or getAddress(right)
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) or getAddress(right)
    elif operator == '=':
        #Convertimos el resultado a string para validar si tiene () y es un apuntador
        resToString = str(res)
        if resToString[0] == '(' and resToString[-1] == ')':
            #Obtenemos la dirección de memoria del apuntador que acabamos de recibir
            res = getAddress(int(resToString[1:-1]))
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) 
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left)
        elif 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) 
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left)
        elif 9000<= res <10000:
            memory.local_ints_stack[-1][res-9000] = getAddress(left)
        elif 10000<= res <11000:
            memory.temp_ints_stack[-1][res-10000] = getAddress(left) 
        elif 11000<= res <12000:
            memory.local_floats_stack[-1][res-11000] = getAddress(left)
        elif 12000<= res <13000:
            memory.temp_floats_stack[-1][res-12000] = getAddress(left) 
        elif 13000<= res <14000:
            memory.local_bools_stack[-1][res-13000] = getAddress(left) 
        elif 14000<= res <15000:
            memory.temp_bools_stack[-1][res-14000] = getAddress(left) 
        elif 21000<= res <22000:
            memory.temp_pointers_stack[-1][res-21000] = getAddress(left)
    #Revisamos si el código de operación es output e imprimimos el contenido de res
    elif operator == 'output':
        print("Output from VM.py")
        print(getAddress(res))
    #Revisamos si el código de operación es input
    elif operator == 'input':
        #declaramos una variable auxiliar en la que recibimos el input
        aux = input()

        if 1000<= res <2000:
            #si el input se puede castear a entero lo guardamos
            try:
                ans = int(aux)
                memory.global_ints[res-1000] = ans 
            except ValueError:
                print("Type error")
                sys.exit()
        elif 3000<= res <4000:
            #si el input se puede castear a float lo guardamos
            try:
                ans = float(aux)
                memory.global_floats[res-3000] = ans 
            except ValueError:
                print("Type error")
                sys.exit()
        elif 7000<= res <8000:
            #El input ya es un string entonces lo guardamos
            memory.global_strings = aux
        elif 9000<= res <10000:
            #si el input se puede castear a entero lo guardamos
            try:
                ans = int(aux)
                memory.local_ints_stack[-1][res-9000] = ans 
            except ValueError:
                print("Type error")
                sys.exit()
        elif 11000<= res <12000:
            #si el input se puede castear a float lo guardamos
            try:
                ans = float(aux)
                memory.local_floats_stack[-1][res-11000] = ans
            except ValueError:
                print("Type error")
                sys.exit()
    #Revisamos si el código de operación es un GOTO
    elif operator == 'GOTO':
        #cambiamos el cuadruplo actual por el que estamos recibiento
        current = res
        continue
    #Revisamos si el código de operación es un GOTOF
    elif operator == 'GOTOF':
        #Revisar si left es falso
        if (getAddress(left) == False):
            #Hacemos el salto
            current = res
            continue
    #Revisamos si el código de operación es un GOSUB
    elif operator == "GOSUB":
        #Llamamos a las funciones reset que empujan a la pila la memoria local y temporal y la liberan para su uso más adelante
        memory.resetLocalMemory();
        memory.resetTempMemory();

        #guardamos el salto que queremos dar
        jump = left
        #guardamos el salto en la pila de saltos
        jumpStack.append(current)
        #guardamos el nombre de la función
        function_name = jump
        #guardamos la posición inicial de la función
        current = vars_table[function_name]['start_position']
        continue
    #Revisamos si el código de operación es un return
    elif operator == "return":
        #guardamos el tipo de función de retorno
        currentType = vars_table[function_name]['type']
        
        #guardamos la posición de memoria de la función
        position = int(vars_table['global']['vars'][function_name]['memory_position'])
        
        #guardamos el valor de retorno como una variable global
        if currentType == 'int':
            memory.global_ints[position-1000] = getAddress(res)
        if currentType == 'float':
            memory.global_floats[position-3000] = getAddress(res)
        if currentType == 'bool':
            memory.global_bools[position-5000] = getAddress(res)
        if currentType == 'string':
            memory.global_strings[position-7000] = getAddress(res)
        
        #Liberamos los stacks de memoria local
        memory.local_ints_stack.pop()
        memory.local_floats_stack.pop()
        memory.local_bools_stack.pop()
        memory.local_strings_stack.pop()

        #liberamos los stacks de memoria temporal
        memory.temp_ints_stack.pop()
        memory.temp_floats_stack.pop()
        memory.temp_bools_stack.pop()
        memory.temp_strings_stack.pop()
        memory.temp_pointers_stack.pop()

        #guardamos el salto
        current = jumpStack.pop() + 1
        paramStack.pop()
        continue
    #Revisamos si el código de operación es un ERA
    elif operator == "ERA":
        #guardamos el nombre de la función
        function_name = left;
        
        #Inicializamos la memoria local según la función que estamos recibiendo
        for i in range (0,vars_table[function_name]['size']['vars']['int']):
            memory.local_ints.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['float']):
            memory.local_floats.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['bool']):
            memory.local_bools.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['string']):
            memory.local_strings.append(None)
        
        #Inicializamos la memoria temporal según la función que estamos recibiendo
        for i in range (0,vars_table[function_name]['size']['vars_temp']['int']):
            memory.local_temp_ints.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['float']):
            memory.local_temp_floats.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['bool']):
            memory.local_temp_bools.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['string']):
            memory.local_temp_strings.append(None)
        
        #guardamos la lista de parámetros de la función
        paramList = list(vars_table[function_name]['vars'])
        #empujamos la lista de parámetros a la pila de parámetros
        paramStack.append(paramList)
    #Revisamos si el código de operación es un PARAMETER
    elif operator == "PARAMETER":
        #guardamos el parámetro
        param = left
        #guardamos el indice del parámetro
        index = int(res)-1
        
        #agregamos los valores de los parámetros a la memoria local según su tipo
        if (len(paramStack[-1]) > 0):
            if 1000<= param <2000 or 9000<= param <11000 or 17000<= param <18000:
                memory.local_ints[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-9000] = getAddress(param)
            if 3000<= param <4000 or 11000<= param <13000 or 18000<= param <19000:
                memory.local_floats[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-11000] = getAddress(param)
            if 5000<= param <6000 or 13000<= param <15000 or 19000<= param <20000:
                memory.local_bools[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-13000] = getAddress(param)
            if 7000<= param <8000 or 15000<= param <17000 or 20000<= param <21000:
                memory.local_strings[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-15000] = getAddress(param)
    #Revisamos si el código de operación es un ENDFUNC
    elif operator == "ENDFUNC":
        #liberamos la memoria local
        memory.local_ints_stack.pop()
        memory.local_floats_stack.pop()
        memory.local_bools_stack.pop()
        memory.local_strings_stack.pop()

        #liberamos la memoria temporal
        memory.temp_ints_stack.pop()
        memory.temp_floats_stack.pop()
        memory.temp_bools_stack.pop()
        memory.temp_strings_stack.pop()
        memory.temp_pointers_stack.pop()
        
        #guardamos el salto
        current = jumpStack.pop() + 1
        paramStack.pop()
        continue
    #Revisamos si el código de operación es un VER
    elif operator == "VER":
        #validamos si la posición que queremos accesar está dentro de los rangos del arreglo
        if getAddress(left) < getAddress(right) or getAddress(left) > getAddress(res):
            print("index out of bounds")
    
    #sumamos uno al contador del while para seguir iterando por los cuadruplos
    current=current+1
