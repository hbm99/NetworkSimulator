from glob import glob
from time import time
from os import getcwd, remove
from bug_catcher.bug_catcher import VerificationSum
from instructions.instruction import IP, Connect, Create, Disconnect, Mac, Ping, Route, Send, SendFrame, SendPacket
from operator import itemgetter

class Simulator:
    
    def __init__(self):
        self.instruction_type = {"connect" : Connect(), "create" : Create(), "disconnect" : Disconnect(), 
                                 "send" : Send(), "mac" : Mac(), "send_frame" : SendFrame(), "ip" : IP(), 
                                 "send_packet" : SendPacket(), "ping" : Ping(), "route" : Route()}
        
        self.bug_catcher_type = {"sum" : VerificationSum()}
        self.bug_catcher = self.bug_catcher_type[self.read_bug_catcher()]
        
        self.ip_dictionary = {}
        
        self.subnetworks = {}
        
        self.computers = {}
        self.hubs = {}
        self.switches = {}
        self.routers = {}
        #se tiene que concebir como un solo diccionario de devices
        
        self.signal_time = self.read_signal_time()/1000
        self.start = time()
        self.instructions = []
        self.read_script()
        self.instructions = sorted(self.instructions, key = itemgetter(0))
        #se tiene lista de instrucciones ordenada por <time> en instructions
    
    def read_bug_catcher(self):
        with open('config.txt') as config:
            error_detection_line = config.readline()
            splitted_line = error_detection_line.split()
            return splitted_line.pop()
    
    def read_signal_time(self):
        with open('config.txt') as config:
            while True:
                line = config.readline()
                if not(line):
                    break
                splitted_line = line.split()
        return int(splitted_line.pop())
    
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
        splitted_name.pop()
        splitted_name = ''.join(splitted_name)
        
        for hub_value in self.hubs.values():
            if splitted_name == hub_value.name:
                for port in hub_value.ports:
                    if port.name == name:
                        return port
        
        for switch_value in self.switches.values():
            if splitted_name == switch_value.name:
                for port in switch_value.ports:
                    if port.name == name:
                        return port
        
        for router_value in self.routers.values():
            if splitted_name == router_value.name:
                for port in router_value.ports:
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