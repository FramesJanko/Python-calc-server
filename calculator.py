import math
import re

oop = {'+': 0, '-': 0, 'x': 1, '/': 1, 'xx': 2}

def add(x, y):
    if type(x) is not float:
        x = float(x)
    if type(y) is not float:
        y = float(y)
    return x + y 

def subtract(x, y):
    return float(x)  - float(y) 

def multiply(x, y):
    return float(x) * float(y)

def divide(x, y):
    return float(x) / float(y)

def power(x, y):
    result = float(x)
    binary = bin(int(y))
    iterable_binary = str(binary)[3:]
    for iteration in iterable_binary:
        result *= result
        if iteration == '1':
            result *=  float(x)
    
    return result

#def sqrt(x, y):
#    time_start = time.perf_counter()
#    sqrt_object = int(x)
#    sqrt_power = int(y)
#    test = sqrt_object + 1
#    temp_sqrt_object = sqrt_object
#    print('beginning test')
#    print(test > sqrt_object)
#    while(test > sqrt_object):
#        temp_sqrt_object = temp_sqrt_object >> 1
#        test = power(temp_sqrt_object, sqrt_power)
#        print(test, sqrt_object)
#    time_stop = time.perf_counter()
#    time_taken = time_stop - time_start
#    print(f'Time elapsed: {time_taken}')
#    return temp_sqrt_object

def sqrt(x):
    result = math.sqrt(float(x))
    return result

def parse_instructions(command) -> float:
    #if str(command[0])[0].isnumeric() or str(command[0]) == '.':
    result = 0.0
    
    if command[1] == '+':
        #print(command[0], command[1], command[2])
        result = add(command[0], command[2])
        return result
    elif command[1] == '-':
        #print(command[0], command[1], command[2])
        result = subtract(command[0],command[2])
        return result
    elif command[1] == 'x':
        #print(command[0], command[1], command[2])
        result = multiply(command[0],command[2])
        return result
    elif command[1] == '/':
        #print(command[0], command[1], command[2])
        result = divide(command[0],command[2])
        return result
    elif command[1] == 'xx':
        #print(command[0], command[1], command[2])
        result = power(command[0],command[2])
        return result
    elif command[1] == '//':
        #print(command[0], command[1])
        result = sqrt(command[0])
        return result
    else:
    #    if command[4] == '+':
    #        result = add(last_result, command[5])
        #print('unknown command')
        return result

def sort_instructions(expressions):
    #create a list of instructions using first term, operator, second term: 'a + b', 'a xx b' etc.
    interim_list = [[i[0],i[4],i[7]] for i in expressions]
    #iterate through the list and fill the empty spaces (such as ['', '/', '4'] 
    #so the first term is the second term of the previous expression.
    #doesn't count additions and subtractions... those start new blocks

    for index in range(len(interim_list)-1):
        if not index == 0:
            if interim_list[index+1][1] == '+' or interim_list[index+1][1] == '-':
                pass
        #print(interim_list[index][1] == '+' or interim_list[index][0] == '-')
        interim_list[index+1][0] = interim_list[index][2] 

    #print(interim_list)
    i = 0
    
    while len(interim_list) > 0:
        if len(interim_list) == 1:
            #print('last one')
            i += 1
            return parse_instructions(interim_list.pop())

        #print(f"list is = {interim_list}, and i = {i}, OOP number: {oop[interim_list[i][1]]}, OOP prev number: {oop[interim_list[i-1][1]]}")
        if (i > 0) and (oop[interim_list[i][1]] == oop[interim_list[i-1][1]]):

            if interim_list[i][1] == 'xx':
                #print("putting first in second")
                interim_list[i-1][2] = parse_instructions(interim_list[i])
                interim_list.remove(interim_list[i])
                i = 0
                continue
            
            #print("putting second in first")
            interim_list[i][0] = parse_instructions(interim_list[i-1])
            interim_list.remove(interim_list[i-1])
            i = 0
            continue

        if (len(interim_list) == i + 1) or (oop[interim_list[i][1]] > oop[interim_list[i+1][1]]):
            if len(interim_list) > i + 1:
                #print(len(interim_list))
                #if interim_list[i+1][1] =='xx':
                #    i += 1
                #    continue
                if i == 0:
                    #print("putting first in second")
                    interim_list[i+1][0] = parse_instructions(interim_list[i])
                    interim_list.remove(interim_list[i])
                    i = 0
                    continue
                else:
                    #print("putting second into first")
                    interim_list[i-1][2] = parse_instructions(interim_list[i])
                    interim_list.remove(interim_list[i])
                    i = 0
                    continue

        if (len(interim_list) == i + 1) or (oop[interim_list[i][1]] < oop[interim_list[i+1][1]]):
            if i > 0:
                if len(interim_list) <= i + 1:
                    #print(f"Interim list is {interim_list} and index is {i}")
                    #print(f"putting {interim_list[i]} in {interim_list[i-1]}")
                    interim_list[i-1][2] = parse_instructions(interim_list[i])
                    interim_list.remove(interim_list[i])
                    i = 0
                    continue

        #print('adding one to while loop')
        i += 1

    #index = 0
    #final_list = []
    #for expression in interim_list:
    #    if index + 1 == len(interim_list):
    #        print(f"this is the last item: {expression}")
    #    if expression[1] == ('-') or expression[1] == '+':
    #        if len(final_list) > 0:
    #            print(f"popping off {final_list[-1][:index]}")
    #        expression_cutoff = 0
    #        print(f"interim list range = {interim_list[index+1:]}")
    #        for cutoff in range(len(interim_list[index+1:])):
    #            if interim_list[index+1:][cutoff][1] == ('-') or interim_list[index+1:][cutoff][1] == '+':
    #                expression_cutoff = max(1, cutoff)
    #                print(f"index + 1 is {index + 1} and cutoff is {expression_cutoff}")
    #                print(f"interim list cutoff {interim_list[index+1:][:expression_cutoff]}")
    #                break
    #        list_item = [expression[0], expression[1],
    #                     interim_list[index+1:][:expression_cutoff]]
    #        print(f"printing list item: {list_item}")
    #        final_list.append(list_item)
    #        print(f"final list so far... {final_list}")
    #        print(f"index is {index} and most inner list is {final_list[-1][index-1:]}")
    #    index += 1
    #        
    #print(final_list)

def calculate(string_of_calculations):
    regex = re.compile(r'((\(?)+(\d+)?\.?\d+(\)?)+)?([^\d\.\(\)]+)((\(?)+((\d+)?\.?\d+)(\)?)+)')
    return sort_instructions(regex.findall(string_of_calculations))

if __name__ == "__main__":
    
    run_program = True
    running_total = 0
    last_result = 0.0
    last_instructions = ()
    compiled_regex = re.compile(r'((\(?)+(\d+)?\.?\d+(\)?)+)?([^\d\.\(\)]+)((\(?)+((\d+)?\.?\d+)(\)?)+)')
    print(f"type of compiled_regex: {type(compiled_regex)}")
    while(run_program):
        value = input()
        if value == 'exit':
            break
        instruction_set = compiled_regex.findall(value) 
        print(f"type of compiled_regex.findall(): {type(instruction_set)}")
        if len(instruction_set) > 0:
            last_instructions = instruction_set 
        print(last_instructions)
        new_instructions = [[last_instructions[item][i] for i in range(len(last_instructions[0]))] for item in range(len(last_instructions))]
        print(new_instructions)
        #print(last_instructions)
        if value == '':
            new_instructions[0][0] = last_result
            last_result = sort_instructions(new_instructions)
        else:
            last_result = sort_instructions(last_instructions)
        #last_result = pemdas(last_instructions, 0)
        print(last_result)
        #for item in last_instructions:
        #    try:
        #        if value == '':
        #            raise ValueError
        #        last_result =pemdas((item[0], item[4], item[7]))
        #        print(last_result)
        #    except ValueError:
        #        print('value error')
        #        last_result = parse_instructions((last_result,item[4],item[7]))
        #        print(last_result)
        #sampleDict = {'col1': [1,2],'col2': [1,3]}
        #df = pd.DataFrame(data=sampleDict)

