
from abc import abstractmethod

from instructions.protocol import ICMP
from network_components.device_utils import Port, Route
from time import time


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
    
    def find_port(self, port_name : str):
        for port in self.ports:
            if port.name == port_name:
                return port
        return None

class IPDevice:
    def __init__(self):
        self.ip_mask_addresses = {}
        self.first_key_ip_mask_addresses = None
        self.first_key_mac_addresses = None
        
    #Returns the IPDevice subnetwork
    def subnetwork_address(self, ip =  None):
        if ip is None:
            ip = self.ip_mask_addresses[self.first_key_ip_mask_addresses][0]
        return bin(int(ip.address, 2) & int(self.ip_mask_addresses[ip.address][1].address, 2))[2:].zfill(32)
    
    #Verifies if IPDevice belongs to the subnetwork
    def is_subnetwork_address(self, possible_subnetwork):
        return self.subnetwork_address() == possible_subnetwork
    
    #Returns IPDevice broadcast address
    def broadcast_address(self):
        
        index_subnetwork = 0
        mask = self.ip_mask_addresses[self.first_key_ip_mask_addresses][1].address
        for i in range(len(mask) - 1, -1, -1):
            if mask[i] != '0':
                index_subnetwork = i
                break
        broadcast_address = [0] * 32
        for i in range(index_subnetwork, len(broadcast_address), 1):
            broadcast_address[i] = 1
        
        broadcast_address = ''.join(broadcast_address)
        broadcast_address = bin(int(self.ip_mask_addresses[self.first_key_ip_mask_addresses][0].address, 2) | int(broadcast_address, 2))
        return broadcast_address
    
class RoutesTableDevice:
    def __init__(self):
        self.routes_table = []
    
    def insert_route(self, route : Route):
        self.routes_table.append(route)
        self.routes_table.sort(key = self.get_1s)
    
    @abstractmethod
    def routing(self, ip_packet):
        pass
        
    def get_1s(self, route : Route):
        return route.route_mask.count("1")
    
    def contains_ip(self, ip : str):
        for route in self.routes_table:
            if route.target_ip == ip:
                return True
        return False
        
            
class Computer(Device, IPDevice, RoutesTableDevice):
    def __init__(self, name, ports_count):
        Device.__init__(self, name)
        IPDevice.__init__(self)
        RoutesTableDevice.__init__(self)
        self.ports = self.create_ports(name, ports_count)
        self.mac_addresses = {}
        self.mac_address = None
        self.txt = self.create_data_txt(self.name)
        self.payload_txt = self.create_payload_txt(self.name)
        self.fill_routes_table(ports_count)
    
    
    def fill_routes_table(self, ports_count):
        if len(self.ip_mask_addresses) == 0:
            return
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
    
    def write_payload_txt(self, name, time, ip, data, protocol_icmp = 0):
        
        control_message = ""
        if protocol_icmp == 1:
            icmp = ICMP()
            control_message = icmp.control_message[int(data, 2)]
        
        with open('devices_txt//' + name + '_payload.txt', 'a') as f:
            i = 8
            f.write(str(time) + " " + str(int(ip.address[0 : i], 2)) + "." + str(int(ip.address[i : 2 * i], 2)) + "." 
                    + str(int(ip.address[2 * i : 3 * i], 2)) + "." + str(int(ip.address[3 * i : 4 * i], 2)) + " " 
                    + hex(int(data, 2)) + " " + control_message + "\n")
            
    def routing(self, ip_packet, simulator = None):
        
        # writting payload txt
        if self.ip_mask_addresses[self.first_key_ip_mask_addresses][0].address == ip_packet.source_ip or ip_packet.source_ip == ip_packet.target_ip: 
            self.write_payload_txt(self.name, int(time() - simulator.start), ip_packet.source_ip, 
                                   ip_packet.payload_data, int(ip_packet.protocol[-1]))
        
        # Verify if payload from icmp is ping
        if ip_packet.protocol == "00000001":
            if ip_packet.payload_data == "00001000":
                # necessary to send pong
                return None, self
            elif ip_packet.payload_data == "00000011":
                return None, None
        
        # stop case, when goal is reached 
        if self.ip_mask_addresses.__contains__(ip_packet.target_ip): 
            target_device = simulator.ip_dictionary[ip_packet.target_ip]
            target_device.write_payload_txt(target_device.name, int(time() - simulator.start), 
                                             ip_packet.source_ip, ip_packet.payload_data, int(ip_packet.protocol[-1]))
            return None, None
        
        # searching if target device is at a subnetwork from the sending host
        for ip_mask in self.ip_mask_addresses.values():
            current_subnetwork = self.subnetwork_address(ip_mask[0])
            target_device : Computer = simulator.ip_dictionary[ip_packet.target_ip.address]
            if current_subnetwork == target_device.subnetwork_address(ip_packet.target_ip):
                target_device.write_payload_txt(target_device.name, int(time() - simulator.start), 
                                                ip_packet.source_ip, ip_packet.payload_data, int(ip_packet.protocol[-1]))
                return None, None
        gateway_ip = self.subnetwork_address()[:-1] + "1"
        
        if gateway_ip not in simulator.ip_dictionary:
            return self, None
        
        gateway_device : RoutesTableDevice = simulator.ip_dictionary[gateway_ip]
        gateway_device.routing(ip_packet, simulator)
        
        
            

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
        
    def routing(self, ip_packet, simulator = None):
        
        for route in self.routes_table:
            
            and_target_ip_route_mask = bin(int(ip_packet.target_ip.address, 2) & int(route.route_mask, 2))[2:].zfill(32)
            target_device = simulator.ip_dictionary[route.target_ip]
            
            if and_target_ip_route_mask == route.target_ip:
                
                sending_port : Port = self.find_port(self.name + "_" + str(route.interface))
                
                current_cable = sending_port.cable
                
                # Selecting cable from duplex cable
                if current_cable.cable_1.port_1.name == sending_port.name:
                    current_cable = current_cable.cable_1
                else :
                    current_cable = current_cable.cable_2
                    
                destination_port : Port = current_cable.port_2
                
                if destination_port.device is IPDevice:
                    ip_packet.target_ip = route.gateway_ip
                    # ip_packet.source_ip = destination_port.device
                    destination_port.device.routing(ip_packet, simulator)
                    return None, None
            
            elif and_target_ip_route_mask == target_device.subnetwork_address():
                target_device.write_payload_txt(target_device.name, int(time() - simulator.start), 
                                                ip_packet.source_ip, ip_packet.payload_data, int(ip_packet.protocol[-1]))
        
        return self, None
        
        


