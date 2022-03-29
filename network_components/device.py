from abc import ABC

from network_components.port import Port

class Device(ABC):
    
    def __init__(self, name):
        self.name = name
        self.txt = self.create_txt(self.name)
        
    def create_txt(self, name : str):
        open(name + '.txt', 'w')
    
    
    def write(self, time : int, port : Port, operation : str, data : str, operation_status : str):
        with open(port.device.name + '.txt', 'a') as f:
            f.write(str(time) + " " + port.name + " " + operation + " " + data + " " + operation_status + "\n")