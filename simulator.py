from glob import glob
from time import time
from os import getcwd, remove
from instructions.connect import Connect
from instructions.create import Create
from instructions.disconnect import Disconnect
from instructions.send import Send
from instructions.mac import Mac
from operator import itemgetter

class Simulator:
    
    def __init__(self):
        self.instruction_type = {"connect" : Connect(), "create" : Create(), "disconnect" : Disconnect(), "send" : Send(), "mac" : Mac()}
        
        self.computers = {}
        self.hubs = {}
        self.switches = {}
        #se puede concebir como un solo diccionario de devices
        
        self.start = time()
        self.instructions = []
        self.read_script()
        self.instructions = sorted(self.instructions, key = itemgetter(0))
        #se tiene lista de instrucciones ordenada por <time> en instructions
    
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
        
        for computer_value in self.computers.values():
            if computer_value.ports[0].name == name:
                return computer_value.ports[0]
        
        splitted_name = name.split('_')
        for hub_value in self.hubs.values():
            if splitted_name[0] == hub_value.name:
                for port in hub_value.ports:
                    if port.name == name:
                        return port

    def run(self):
        cwd = getcwd()
        txt_files = glob(cwd + '//devices_txt/' + '/*.txt')
        for txt_file in txt_files:
            remove(txt_file)
        
        while len(self.instructions) > 0:
            if self.instructions[0][0] <= time() - self.start: #time to take instruction <= elapsed seconds #elapsed_seconds = time.time() - start #elapsed_milliseconds = elapsed_seconds * 1000
                current_instruction = self.instruction_type[self.instructions[0][1]] #parse instruction
                current_instruction.execute(self, self.instructions[0]) #execute instruction
                self.instructions.pop(0)