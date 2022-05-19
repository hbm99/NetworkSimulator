from abc import ABC

from numpy import broadcast

from network_components.device_utils import IPAddress, MacAddress, Port, SubnetworkMask


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
        self.ports = [Port(name + "_" + str(1), self)]
        self.mac_address = MacAddress("")
        self.ip = IPAddress("")
        self.subnetwork_mask = SubnetworkMask("")
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
    
    #Returns the host subnetwork
    def subnetwork_address(self):
        bin_ip = bin(self.ip.address)
        bin_mask = bin(self.subnetwork_mask.address)
        return bin_ip & bin_mask
    
    #Verifies if host belongs to the subnetwork
    def is_subnetwork_address(self, possible_subnetwork):
        return self.subnetwork_address() == possible_subnetwork
    
    #Returns host broadcast address
    def broadcast_address(self):
        index_subnetwork = 0
        for i in range(len(self.subnetwork_mask.address)):
            if self.subnetwork_mask.address[i] == '0':
                index_subnetwork = i
                break
        broadcast_address = [0] * 32
        for i in range(index_subnetwork, len(broadcast_address), 1):
            broadcast_address[i] = 1
        for i in range(broadcast_address):
            broadcast_address[i] = int(self.ip.address) | broadcast_address[i]
        return bin(str(broadcast_address))
            
class Hub(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
    
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports.append(Port(name + "_" + str(i + 1), self))
        return ports
    
class Switch(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
        self.mac_addresses = {}
    
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports.append(Port(name + "_" + str(i + 1), self))
        return ports

