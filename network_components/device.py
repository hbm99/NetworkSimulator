from abc import ABC
import network_components.device_utils as device_utils

class Device(ABC):
    def __init__(self, name):
        self.name = name
        self.txt = self.create_txt(self.name)
        
    def create_txt(self, name : str):
        open('devices_txt//' + name + '.txt', 'w')
    
    def write_txt(self, time : int, port, operation : str, data : str, operation_status : str):
        with open('devices_txt//' + port.device.name + '.txt', 'a') as f:
            f.write(str(time) + " " + port.name + " " + operation + " " + data + " " + operation_status + "\n")
            
class Computer(Device):
    def __init__(self, name):
        super().__init__(name)
        self.ports = [device_utils.Port(name + "_" + str(1), self)]
        self.mac_address = device_utils.MacAddress("")
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
            
class Hub(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
    
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports.append(device_utils.Port(name + "_" + str(i + 1), self))
        return ports
    
class Switch(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
        self.mac_addresses = {}
    
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports.append(device_utils.Port(name + "_" + str(i + 1), self))
        return ports

