from network_components.device import Device
from network_components.mac_address import MacAddress
from network_components.port import Port


class Computer(Device):
    def __init__(self, name):
        super().__init__(name)
        self.ports = [Port(name + "_" + str(1), self)]
        self.mac_address = MacAddress("")
        self.txt = self.create_data_txt(self.name)
    
    def create_data_txt(self, name : str):
        open('devices_txt//' + name + '_data.txt', 'w')
        
    def write_data_txt(self, time, name : str, mac_address : str, data : str, corrupted_data : bool):
        with open('devices_txt//' + name + '_data.txt', 'a') as f:
            error_signal = ""
            if corrupted_data:
                error_signal += "ERROR\n"
            else : 
                error_signal += "\n"
            f.write(str(time) + " " + hex(int(mac_address, 2)) + " " + data + " " + error_signal)
            
                
            
