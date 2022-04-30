from abc import ABC

from network_components.port import Port

class Device(ABC):
    
    def __init__(self, name):
        self.name = name
        self.txt = self.create_txt(self.name)
        
    def create_txt(self, name : str):
        open('devices_txt//' + name + '.txt', 'w')
        open('devices_txt//' + name + '_data.txt', 'w')
    
    
    def write_txt(self, time : int, port : Port, operation : str, data : str, operation_status : str):
        with open('devices_txt//' + port.device.name + '.txt', 'a') as f:
            f.write(str(time) + " " + port.name + " " + operation + " " + data + " " + operation_status + "\n")
    
    def write_data_txt(self, time, name : str, mac_address : str, data : str):
        with open('devices_txt//' + name + '_data.txt', 'a') as f:
            f.write(str(time) + " " + hex(int(mac_address, 2)) + " " + data + "\n")