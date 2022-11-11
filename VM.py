from MemoryManager import MemoryManager
import parserv2

memory = MemoryManager()

tables = parserv2.run()

constants_table = tables[0]
vars_table = tables[1]
num_temps = tables[2]

quad_list = []

with open("output.sgo") as file:
    for line in file:
        temp = line.split(' ')
        
        operator = temp[3]
        
        left = temp[5]
        if left != 'None':
            left = int(temp[5])
            
        right = temp[7]
        if right != 'None':
            right = int(temp[7])

        res = temp[9]
        if res != 'None':
            res = int(temp[9])

        quad = [operator, left, right, res]
        quad_list.append(quad)

print(quad_list)

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
        memory.global_ints.append(None)
    if vars_table['global']['vars'][var]['type'] == 'float':
        memory.global_floats.append(None)
    if vars_table['global']['vars'][var]['type'] == 'bool':
        memory.global_bools.append(None)
    if vars_table['global']['vars'][var]['type'] == 'string':
        memory.global_strings.append(None)
        
for i in range(0, num_temps['int']):
    memory.local_temp_ints.append(None)
for i in range(0, num_temps['float']):
    memory.local_temp_floats.append(None)
for i in range(0, num_temps['bool']):
    memory.local_temp_bools.append(None)
for i in range(0, num_temps['string']):
    memory.local_temp_strings.append(None)


def getAddress(addr): 
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
        if memory.local_ints[addr-9000] == None:
            return
        return memory.local_ints[addr-9000]
    elif 10000<=addr<11000:
        if memory.local_temp_ints[addr-10000] == None:
            return
        return memory.local_temp_ints[addr-10000]
    elif 11000<=addr<12000:
        if memory.local_floats[addr-11000] == None:
            return
        return memory.local_floats[addr-11000]
    elif 12000<=addr<13000:
        if memory.local_temp_floats[addr-12000] == None:
            return
        return memory.local_temp_floats[addr-12000]
    elif 13000<=addr<14000:
        if memory.local_bools[addr-13000] == None:
            return
        return memory.local_bools[addr-13000]
    elif 14000<=addr<15000:
        if memory.local_temp_bools[addr-14000] == None:
            return
        return memory.local_temp_bools[addr-14000]
    elif 15000<=addr<16000:
        if memory.local_strings[addr-15000] == None:
            return
        return memory.local_strings[addr-15000]
    elif 16000<=addr<17000:
        if memory.local_temp_strings[addr-16000] == None:
            return
        return memory.local_temp_strings[addr-16000]
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
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) + getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) + getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-9000] = getAddress(left) + getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-10000] = getAddress(left) + getAddress(right)
    elif operator == '-':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) - getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) - getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) - getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) - getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) - getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) - getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-9000] = getAddress(left) - getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-10000] = getAddress(left) - getAddress(right)
    elif operator == '*':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) * getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) * getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) * getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) * getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) * getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) * getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-9000] = getAddress(left) * getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-10000] = getAddress(left) * getAddress(right)
    elif operator == '/':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) / getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) / getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) / getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) / getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) / getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) / getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-9000] = getAddress(left) / getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-10000] = getAddress(left) / getAddress(right)
    elif operator == '>':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) > getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) > getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) > getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) > getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) > getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) > getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) > getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) > getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) > getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) > getAddress(right)
    elif operator == '<':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) < getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) < getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) < getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) < getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) < getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) < getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) < getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) < getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) < getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) < getAddress(right)
    elif operator == '>=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) >= getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) >= getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) >= getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) >= getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) >= getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) >= getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) >= getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) >= getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) >= getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) >= getAddress(right)
    elif operator == '<=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) <= getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) <= getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) <= getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) <= getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) <= getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) <= getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) <= getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) <= getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) <= getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) <= getAddress(right)
    elif operator == '<=':
        if 1000<= res <2000:
            memory.global_ints[res-1000] = getAddress(left) <= getAddress(right)
        elif 2000<= res <3000:
            memory.global_temp_ints[res-2000] = getAddress(left) <= getAddress(right)
        elif 3000<= res <4000:
            memory.global_floats[res-3000] = getAddress(left) <= getAddress(right)
        elif 4000<= res <5000:
            memory.global_temp_floats[res-4000] = getAddress(left) <= getAddress(right)
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) <= getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) <= getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) <= getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) <= getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) <= getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) <= getAddress(right)
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
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) == getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) == getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) == getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) == getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) == getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) == getAddress(right)
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
        elif 9000<= res <1000:
            memory.local_ints[res-9000] = getAddress(left) != getAddress(right)
        elif 10000<= res <11000:
            memory.local_temp_ints[res-10000] = getAddress(left) != getAddress(right)
        elif 11000<= res <12000:
            memory.local_floats[res-11000] = getAddress(left) != getAddress(right)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-12000] = getAddress(left) != getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) != getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) != getAddress(right)
    elif operator == '&&':
        if 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) != getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) != getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) != getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) != getAddress(right)
    elif operator == '||':
        if 5000<= res <6000:
            memory.global_bools[res-5000] = getAddress(left) != getAddress(right)
        elif 6000<= res <7000:
            memory.global_temp_bools[res-6000] = getAddress(left) != getAddress(right)
        elif 13000<= res <14000:
            memory.local_bools[res-13000] = getAddress(left) != getAddress(right)
        elif 14000<= res <15000:
            memory.local_temp_bools[res-14000] = getAddress(left) != getAddress(right)
    elif operator == '=':
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
        elif 9000<= res < 1000:
            memory.local_ints[res-9000] = getAddress(left)
        elif 10000<=res<11000:
            memory.local_temp_ints[res-10000] = getAddress(left)
        elif 11000<= res <12000:
            memory.local_floats[res-9000] = getAddress(left)
        elif 12000<= res <13000:
            memory.local_temp_floats[res-10000] = getAddress(left)
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
    current=current+1
            
            
                
                 
                
            
        

        

    
    
        

