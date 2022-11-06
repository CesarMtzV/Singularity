from MemoryManager import MemoryManager

memory = MemoryManager()

memory.global_ints.append(None)
memory.global_temp_ints.append(None)
memory.const_ints.append(None)
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
    
with open("output.sgo") as file:
    for line in file:
        temp = line.split(' ')
        
        operator = temp[1]
        
        left = temp[3]
        if left != 'None':
            left = int(temp[3])
            
        right = temp[5]
        if right != 'None':
            right = int(temp[5])

        res = int(temp[7])
        
        if operator == '+':
            if 1000<= res <2000:
                memory.global_ints[res-1000] = getAddress(left) + getAddress(right)
            elif 2000<= res <3000:
                memory.global_temp_ints[res-2000] = getAddress(left) + getAddress(right)
            elif 3000<= res <4000:
                memory.global_floats[res-3000] = getAddress(left) + getAddress(right)
            elif 4000<= res <5000:
                memory.global_temp_floats[res-4000] = getAddress(left) + getAddress(right)
        elif operator == '-':
            if 1000<= res <2000:
                memory.global_ints[res-1000] = getAddress(left) - getAddress(right)
            elif 2000<= res <3000:
                memory.global_temp_ints[res-2000] = getAddress(left) - getAddress(right)
            elif 3000<= res <4000:
                memory.global_floats[res-3000] = getAddress(left) - getAddress(right)
            elif 4000<= res <5000:
                memory.global_temp_floats[res-4000] = getAddress(left) - getAddress(right)
        elif operator == '*':
            if 1000<= res <2000:
                memory.global_ints[res-1000] = getAddress(left) * getAddress(right)
            elif 2000<= res <3000:
                memory.global_temp_ints[res-2000] = getAddress(left) * getAddress(right)
            elif 3000<= res <4000:
                memory.global_floats[res-3000] = getAddress(left) * getAddress(right)
            elif 4000<= res <5000:
                memory.global_temp_floats[res-4000] = getAddress(left) * getAddress(right)
        elif operator == '/':
            if 1000<= res <2000:
                memory.global_ints[res-1000] = getAddress(left) / getAddress(right)
            elif 2000<= res <3000:
                memory.global_temp_ints[res-2000] = getAddress(left) / getAddress(right)
            elif 3000<= res <4000:
                memory.global_floats[res-3000] = getAddress(left) / getAddress(right)
            elif 4000<= res <5000:
                memory.global_temp_floats = getAddress(left) / getAddress(right)
        elif operator == '=':
            if 1000<= res <2000:
                memory.global_ints[res-1000] = getAddress(left) 
            elif 2000<= res <3000:
                memory.global_temp_ints[res-2000] = getAddress(left)
            elif 3000<= res <4000:
                memory.global_floats[res-3000] = getAddress(left)
            elif 4000<= res <5000:
                memory.global_temp_floats[res-4000] = getAddress(left)
        elif operator == 'output':
            print(memory.global_ints)
            print(res)
            print(getAddress(res))
            
                
                 
                
            
        

        

    
    
        

