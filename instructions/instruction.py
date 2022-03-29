from abc import ABC, abstractmethod
from main import simulator

class Instruction(ABC):
    
    @abstractmethod
    def execute(self, args):
        pass
    
    def find_port(name : str):
        for i in range(len(simulator.computers)):
            if simulator.computers[i].port.name == name:
                return simulator.computers[i].port
        for i in range(len(simulator.hubs)):
            splitted_name = name.split('_')
            if splitted_name[0] == simulator.hubs[i].name:
                for j in range(len(simulator.hubs[i].ports)):
                    if simulator.hubs[i].ports[j].name == splitted_name[1]:
                        return simulator.hubs[i].ports[j]
 