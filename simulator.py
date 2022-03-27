import time
from instructions.connect import Connect
from instructions.create import Create
from instructions.disconnect import Disconnect
from instructions.send import Send

class Simulator:
    
    def __init__(self):
        self.instruction_type = {"connect" : Connect(), "create" : Create(), "disconnect" : Disconnect(), "send" : Send()}
        self.computers = []
        self.hubs = []
        self.start = time.time()
        self.instructions = []
        self.read_script()
        self.instructions.sort(key = self.instruction_time)
        #se tiene lista de instrucciones ordenada por <time> en instructions
        
    def instruction_time(element):
        return element[0]
    
    def read_script(self):
        with open('script.txt') as script:
            while True:
                line = script.readline()
                if not(line):
                    break
                splitted_line = line.split()
                splitted_line[0] = int(splitted_line[0])
                self.instructions.append(splitted_line)
                
    def start_time(self):
        return self.start
                
    def execute(self):
        while len(self.instructions) > 0:
            if self.instructions[0][0] <= time.time() - self.start: #time to take instruction <= elapsed seconds #elapsed_seconds = time.time() - start #elapsed_milliseconds = elapsed_seconds * 1000
                current_instruction = self.instruction_type[self.instructions[0][1]] #parse instruction
                current_instruction.execute(self.instructions[0]) #execute instruction
                self.instructions.pop(0)
            index += 1
    

""" instruction_type = {"connect" : Connect(), "create" : Create(), "disconnect" : Disconnect(), "send" : Send()}

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


index = 0
while len(instructions) > 0:
    if instructions[0][0] <= time.time() - start: #time to take instruction <= elapsed seconds #elapsed_seconds = time.time() - start #elapsed_milliseconds = elapsed_seconds * 1000
        current_instruction = instruction_type[instructions[index][1]] #parse instruction
        current_instruction.execute(instructions[index]) #execute instruction
        instructions.pop(0)
    index += 1 """
