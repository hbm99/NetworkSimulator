from network_components.device_utils import Port


class Device:
    def __init__(self, name):
        self.name = name
        self.txt = self.create_txt(self.name)
        
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports.append(Port(name + "_" + str(i + 1), self))
        return ports
        
    def create_txt(self, name : str):
        open('devices_txt//' + name + '.txt', 'w')
    
    def write_txt(self, time : int, port, operation : str, data : str, operation_status : str):
        with open('devices_txt//' + port.device.name + '.txt', 'a') as f:
            f.write(str(time) + " " + port.name + " " + operation + " " + data + " " + operation_status + "\n")
            
class IPDevice:
    def __init__(self):
        self.ip_mask_addresses = {} # IPAddress("")
        # self.subnetwork_mask = ∫SubnetworkMask("")
        
    #Returns the IPDevice subnetwork
    def subnetwork_address(self):
        first_key = next(iter(self.ip_mask_addresses))
        bin_ip = bin(self.ip_mask_addresses[first_key][0].address)
        bin_mask = bin(self.ip_mask_addresses[first_key][1].address)
        return bin_ip & bin_mask
    
    #Verifies if IPDevice belongs to the subnetwork
    def is_subnetwork_address(self, possible_subnetwork):
        return self.subnetwork_address() == possible_subnetwork
    
    #Returns IPDevice broadcast address
    def broadcast_address(self):
        first_key = next(iter(self.ip_mask_addresses))
        index_subnetwork = 0
        mask = self.ip_mask_addresses[first_key][1].address
        for i in range(len(mask) - 1, -1, -1):
            if mask[i] != '0':
                index_subnetwork = i
                break
        broadcast_address = [0] * 32
        for i in range(index_subnetwork, len(broadcast_address), 1):
            broadcast_address[i] = 1
        for i in range(broadcast_address):
            broadcast_address[i] = int(self.ip_mask_addresses[first_key][0].address) | broadcast_address[i]
        return bin(str(broadcast_address))
            
class Computer(Device, IPDevice):
    def __init__(self, name, ports_count):
        Device.__init__(self, name)
        IPDevice.__init__(self)
        self.ports = self.create_ports(name, ports_count)
        self.mac_addresses = {}
        self.txt = self.create_data_txt(self.name)
        self.payload_txt = self.create_payload_txt(self.name)
    
    def create_data_txt(self, name : str):
        open('devices_txt//' + name + '_data.txt', 'w')
    
    def create_payload_txt(self, name : str):
        open('devices_txt//' + name + '_payload.txt', 'w')
        
    def write_data_txt(self, time, name : str, mac_address : str, data : str, corrupted_data : bool):
        with open('devices_txt//' + name + '_data.txt', 'a') as f:
            error_signal = ""
            if corrupted_data:
                error_signal += "ERROR\n"
            else : 
                error_signal += "\n"
            f.write(str(time) + " " + hex(int(mac_address, 2)) + " " + data + " " + error_signal)
    
    def write_payload_txt(self, name, time, ip, data):
        with open('devices_txt//' + name + '_payload.txt', 'a') as f:
            f.write(str(time) + " " + int(ip, 2) + " " + data + "\n")
            
            
class Hub(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
    
class Switch(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
        self.mac_addresses = {}
    
class Router(Device, IPDevice):
    def __init__(self, name, ports_count):
        Device.__init__(self, name)
        IPDevice.__init__(self)
        self.ports = self.create_ports(name, int(ports_count))

    


