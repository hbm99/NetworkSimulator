from time import time
from instructions.connect import Connect
from instructions.create import Create
from instructions.disconnect import Disconnect
from instructions.send import Send
from operator import itemgetter
from network_components.computer.computer import Computer
from network_components.device import Device
from network_components.hub import Hub

class Simulator:
    
    def __init__(self):
        self.instruction_type = {"connect" : Connect(), "create" : Create(), "disconnect" : Disconnect(), "send" : Send()}
        self.computers = []
        self.hubs = []
        self.start = time()
        self.instructions = []
        self.read_script()
        self.instructions = sorted(self.instructions, key = itemgetter(0))
        #se tiene lista de instrucciones ordenada por <time> en instructions
        self.signal_time = 10
    
    def read_script(self):
        with open('script.txt') as script:
            while True:
                line = script.readline()
                if not(line):
                    break
                splitted_line = line.split()
                splitted_line[0] = int(splitted_line[0])
                self.instructions.append(splitted_line)

    def find_port(self, name : str):
        for i in range(len(self.computers)):
            if self.computers[i].ports[0].name == name:
                return self.computers[i].ports[0]
        for i in range(len(self.hubs)):
            splitted_name = name.split('_')
            if splitted_name[0] == self.hubs[i].name:
                for j in range(len(self.hubs[i].ports)):
                    if self.hubs[i].ports[j].name == name:
                        return self.hubs[i].ports[j]
    
    # def add_device(self, device : Device):
    #     if isinstance(device, Hub):
    #         self.hubs.append(device)
    #     elif isinstance(device, Computer):
    #         self.computers.append(device)

    def run(self):
        while len(self.instructions) > 0:
            if self.instructions[0][0] <= time() - self.start: #time to take instruction <= elapsed seconds #elapsed_seconds = time.time() - start #elapsed_milliseconds = elapsed_seconds * 1000
                current_instruction = self.instruction_type[self.instructions[0][1]] #parse instruction
                current_instruction.execute(self, self.instructions[0]) #execute instruction
                self.instructions.pop(0)
    

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
