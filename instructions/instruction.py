from abc import ABC, abstractmethod
from simulator import computers, hubs

class Instruction(ABC):
    
    @abstractmethod
    def execute(self, args):
        pass
    
    def find_port(name : str):
        for i in range(len(computers)):
            if computers[i].port.name == name:
                return computers[i].port
        for i in range(len(hubs)):
            splitted_name = name.split('_')
            if splitted_name[0] == hubs[i].name:
                for j in range(len(hubs[i].ports)):
                    if hubs[i].ports[j].name == splitted_name[1]:
                        return hubs[i].ports[j]
 