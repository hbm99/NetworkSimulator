import time

computers = []
hubs = []

start = time.time()

instructions = []
with open('script.txt') as script:
    while True:
        line = script.readline()
        if not(line):
            break
        splitted_line = line.split()
        splitted_line[0] = int(splitted_line[0])
        instructions.append(splitted_line)

def instruction_time(element):
    return element[0]

instructions.sort(key = instruction_time)
#se tiene lista de instrucciones ordenada por <time> en instructions

while len(instructions) > 0:
    
    if instructions[0][0] <= time.time() - start: #time to take instruction <= elapsed seconds #elapsed_seconds = time.time() - start #elapsed_milliseconds = elapsed_seconds * 1000
        #parse/execute instruction
        instructions.pop(0)

        

