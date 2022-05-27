
from abc import abstractmethod
from network_components.device_utils import Port, Route


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
    def find_port(port_name : str):
        # a implementar, ver llamado en routing de router
        return
            
class IPDevice:
    def __init__(self):
        self.ip_mask_addresses = {}
        self.first_key = next(iter(self.ip_mask_addresses))
        
    #Returns the IPDevice subnetwork
    def subnetwork_address(self):
        bin_ip = bin(self.ip_mask_addresses[self.first_key][0].address)
        bin_mask = bin(self.ip_mask_addresses[self.first_key][1].address)
        return bin_ip & bin_mask
    
    #Verifies if IPDevice belongs to the subnetwork
    def is_subnetwork_address(self, possible_subnetwork):
        return self.subnetwork_address() == possible_subnetwork
    
    #Returns IPDevice broadcast address
    def broadcast_address(self):
        
        index_subnetwork = 0
        mask = self.ip_mask_addresses[self.first_key][1].address
        for i in range(len(mask) - 1, -1, -1):
            if mask[i] != '0':
                index_subnetwork = i
                break
        broadcast_address = [0] * 32
        for i in range(index_subnetwork, len(broadcast_address), 1):
            broadcast_address[i] = 1
        for i in range(broadcast_address):
            broadcast_address[i] = int(self.ip_mask_addresses[self.first_key][0].address) | broadcast_address[i]
        return bin(str(broadcast_address))
    
class RoutesTableDevice:
    def __init__(self):
        self.routes_table = []
    def insert_route(self, route : Route):
        self.routes_table(route)
        self.routes_table.sort(self.instructions, key = self.get_1s)
    @abstractmethod
    def routing(self, ip_packet):
        pass
        
    def get_1s(route : Route):
        return route.route_mask.count("1")
            
class Computer(Device, IPDevice, RoutesTableDevice):
    def __init__(self, name, ports_count):
        Device.__init__(self, name)
        IPDevice.__init__(self)
        RoutesTableDevice.__init__(self)
        self.ports = self.create_ports(name, ports_count)
        self.mac_addresses = {}
        self.txt = self.create_data_txt(self.name)
        self.payload_txt = self.create_payload_txt(self.name)
        self.fill_routes_table(ports_count)
    
    
    def fill_routes_table(self, ports_count):
        subnetwork_address = self.subnetwork_address()
        subnetwork_route = Route(subnetwork_address, self.ip_mask_addresses[next(iter(self.ip_mask_addresses))], "0" * 32, ports_count)
        self.insert_route(subnetwork_route)
        default_route = Route("0" * 32, "0" * 32, subnetwork_address[:-1] + "1", ports_count)
        self.insert_route(default_route)
    
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
            i = 8
            f.write(str(time) + " " + int(ip[0 : i], 2) + "." + int(ip[i : 2 * i], 2) + "." 
                    + int(ip[2 * i : 3 * i], 2) + "." + int(ip[3 * i : 4 * i], 2) + "." + " " 
                    + data + "\n")
            
    def routing(self, ip_packet):
        # nos quedamos aquí
        return
            

class Hub(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
    
class Switch(Device):
    def __init__(self, name, ports_count):
        super().__init__(name)
        self.ports = self.create_ports(name, int(ports_count))
        self.mac_addresses = {}
    
class Router(Device, IPDevice, RoutesTableDevice):
    def __init__(self, name, ports_count):
        Device.__init__(self, name)
        IPDevice.__init__(self)
        RoutesTableDevice.__init__(self)
        self.ports = self.create_ports(name, int(ports_count))
        
    def routing(self, ip_packet):
        
        # if self.ip_mask_addresses.__contains__(ip_packet.target_ip): # este caso no debe ocurrir aquí porque debe terminar en un host, no en un router
        #     return None
        
        for route in self.routes_table:
            and_target_ip_route_mask = bin(int(ip_packet.target_ip, 2)) & bin(int(route.route_mask, 2))
            if str(and_target_ip_route_mask) == route.target_ip:
                
                sending_port : Port = self.find_port(self.name + "_" + str(route.interface)) # implementar método que a partir del nombre devuelve el puerto
                
                current_cable = sending_port.cable
                
                # Selecting cable from duplex cable
                if current_cable.cable_1.port_1.name == sending_port.name:
                    current_cable = current_cable.cable_1
                else :
                    current_cable = current_cable.cable_2
                    
                destination_port : Port = current_cable.port_2
                
                if destination_port.device is IPDevice:
                    ip_packet.target_ip = route.gateway_ip
                    ip_packet.source_ip = destination_port.device
                    destination_port.device.routing(ip_packet)
                    return None
        
        return self
        
        


