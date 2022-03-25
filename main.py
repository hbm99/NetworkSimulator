import time

start = time.time()

instructions = []
with open('script.txt') as script:
    line = script.readline()
    splitted_line = line.split()
    splitted_line[0] = int(splitted_line[0])
    instructions.append(splitted_line)
    while line:
        line = script.readline()
        splitted_line = line.split()
        splitted_line[0] = int(splitted_line[0])
        instructions.append(splitted_line)

def instruction_time(element):
    return element[0]

instructions.sort(key = instruction_time)

#se tiene lista de instrucciones ordenada por <time> en instructions
while True:
    
    elapsed_seconds = time.time() - start
    elapsed_milliseconds = elapsed_seconds * 1000
    
    