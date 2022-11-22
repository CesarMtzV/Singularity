from MemoryManager import MemoryManager
import parserv2

memory = MemoryManager()

tables = parserv2.run()

constants_table = tables[0]
vars_table = tables[1]
num_temps = tables[2]

quad_list = []
function_name = ' '
jumpStack = []
paramList = []
paramStack = []

with open("output.sgo") as file:
    for line in file:
        temp = line.split(' ')
        
        operator = temp[3]
        
        left = temp[5]
        if left.isdigit():
            left = int(temp[5])
            
        right = temp[7]
        if right != 'None':
            right = int(temp[7])

        res = temp[9]
        if res.isdigit():
            res = int(temp[9])

        quad = [operator, left, right, res]
        quad_list.append(quad)

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

for var in vars_table['global']['vars']:
    if vars_table['global']['vars'][var]['type'] == 'int':
        if 'limit_1' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])+1):
                memory.global_ints.append(None)
        if 'limit_2' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])*int(vars_table['global']['vars'][var]['limit_2'])+1):
                memory.global_ints.append(None)
        else:
            memory.global_ints.append(None)
    if vars_table['global']['vars'][var]['type'] == 'float':
        if 'limit_1' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])+1):
                memory.global_floats.append(None)
        if 'limit_2' in vars_table['global']['vars'][var]:
            for i in range(0,int(vars_table['global']['vars'][var]['limit_1'])*int(vars_table['global']['vars'][var]['limit_2'])+1):
                memory.global_floats.append(None)
        else:
            memory.global_floats.append(None)
    if vars_table['global']['vars'][var]['type'] == 'bool':
        memory.global_bools.append(None)
    if vars_table['global']['vars'][var]['type'] == 'string':
        memory.global_strings.append(None)
        
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
    
memory.resetLocalMemory();
memory.resetTempMemory();

def getAddress(addr):
    addressToString = str(addr)
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
        
    
current = 0
while current < len(quad_list):
    operator = quad_list[current][0]
    left = quad_list[current][1]
    right = quad_list[current][2]
    res = quad_list[current][3]
    
    if operator == '+':
        if 1000<= res <2000:
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
        resToString = str(res)
        if resToString[0] == '(' and resToString[-1] == ')':
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
    elif operator == 'output':
        print("Output from VM.py")
        print(getAddress(res))
    elif operator == 'GOTO':
        current = res
        continue
    elif operator == 'GOTOF':
        if (getAddress(left) == False):
            current = res
            continue
    elif operator == "GOSUB":
        memory.resetLocalMemory();
        memory.resetTempMemory();

        jump = left
        jumpStack.append(current)
        function_name = jump
        current = vars_table[function_name]['start_position']
        continue
    elif operator == "return":
        currentType = vars_table[function_name]['type']
        
        position = int(vars_table['global']['vars'][function_name]['memory_position'])
        
        if currentType == 'int':
            memory.global_ints[position-1000] = getAddress(res)
        if currentType == 'float':
            memory.global_floats[position-3000] = getAddress(res)
        if currentType == 'bool':
            memory.global_bools[position-5000] = getAddress(res)
        if currentType == 'string':
            memory.global_strings[position-7000] = getAddress(res)
            
        memory.local_ints_stack.pop()
        memory.local_floats_stack.pop()
        memory.local_bools_stack.pop()
        memory.local_strings_stack.pop()

        memory.temp_ints_stack.pop()
        memory.temp_floats_stack.pop()
        memory.temp_bools_stack.pop()
        memory.temp_strings_stack.pop()
        memory.temp_pointers_stack.pop()

        
        current = jumpStack.pop() + 1
        paramStack.pop()
        continue
        
    elif operator == "ERA":
        function_name = left;
        
        for i in range (0,vars_table[function_name]['size']['vars']['int']):
            memory.local_ints.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['float']):
            memory.local_floats.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['bool']):
            memory.local_bools.append(None)
        for i in range (0,vars_table[function_name]['size']['vars']['string']):
            memory.local_strings.append(None)
        
        for i in range (0,vars_table[function_name]['size']['vars_temp']['int']):
            memory.local_temp_ints.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['float']):
            memory.local_temp_floats.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['bool']):
            memory.local_temp_bools.append(None)
        for i in range (0,vars_table[function_name]['size']['vars_temp']['string']):
            memory.local_temp_strings.append(None)
        
        paramList = list(vars_table[function_name]['vars'])
        paramStack.append(paramList)
            
    elif operator == "PARAMETER":
        param = left
        index = int(res)-1
        
        if (len(paramStack[-1]) > 0):
            if 1000<= param <2000 or 9000<= param <11000 or 17000<= param <18000:
                memory.local_ints[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-9000] = getAddress(param)
            if 3000<= param <4000 or 11000<= param <13000 or 18000<= param <19000:
                memory.local_floats[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-11000] = getAddress(param)
            if 5000<= param <6000 or 13000<= param <15000 or 19000<= param <20000:
                memory.local_bools[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-13000] = getAddress(param)
            if 7000<= param <8000 or 15000<= param <17000 or 20000<= param <21000:
                memory.local_strings[vars_table[function_name]['vars'][paramStack[-1][index]]['memory_position']-15000] = getAddress(param)
    elif operator == "ENDFUNC":
        memory.local_ints_stack.pop()
        memory.local_floats_stack.pop()
        memory.local_bools_stack.pop()
        memory.local_strings_stack.pop()

        memory.temp_ints_stack.pop()
        memory.temp_floats_stack.pop()
        memory.temp_bools_stack.pop()
        memory.temp_strings_stack.pop()
        memory.temp_pointers_stack.pop()
        
        current = jumpStack.pop() + 1
        paramStack.pop()
        continue
    elif operator == "VER":
        if getAddress(left) < getAddress(right) or getAddress(left) > getAddress(res):
            print("index out of bounds")
    
    
    current=current+1
            
            
                
                 
                
            
        

        

    
    
        

