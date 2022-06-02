from abc import ABC, abstractmethod
from time import time, sleep

from instructions.protocol import ARP, ICMP
from network_components.device import Computer, Hub, Router, Switch
from network_components.device_utils import DuplexCable, Frame, IPAddress, IPPacket, MacAddress, Port, Subnetwork, SubnetworkMask


class Instruction(ABC):
    
    @abstractmethod
    def execute(self, simulator, args):
        pass
 

class Create(Instruction):
    
    def execute(self, simulator, args):
        if args[2] == "hub":
            hub = Hub(args[3], args[4])
            simulator.hubs[args[3]] = hub
        elif args[2] == "host":
            name_interface = args[3].split(':')
            interface = 1
            if len(name_interface) == 2:
                interface = int(name_interface[1])
            computer = Computer(name_interface[0], interface)
            simulator.computers[name_interface[0]] = computer
        elif args[2] == "switch":
            switch = Switch(args[3], args[4])
            simulator.switches[args[3]] = switch
        elif args[2] == "router":
            router = Router(args[3], args[4])
            simulator.routers[args[3]] = router
            
class Connect(Instruction):
    
    def execute(self, simulator, args):
        port_1 = simulator.find_port(args[2])
        port_2 = simulator.find_port(args[3])
        wire = DuplexCable(port_1, port_2)
        port_1.cable = wire
        port_2.cable = wire

class Disconnect(Instruction):
    
    def execute(self, simulator, args):
        port = simulator.find_port(args[2])
        duplex_cable = port.cable
        if duplex_cable.cable_1.port_1.name == port.name:
            duplex_cable.cable_1.port_1 = None
            duplex_cable.cable_2.port_2 = None
        else : 
            duplex_cable.cable_1.port_2 = None
            duplex_cable.cable_2.port_1 = None
        port.cable = None
        
class Mac(Instruction):
    
    def execute(self, simulator, args):
        address = bin(int(args[3], 16))[2:]
        mac_address = MacAddress(address)
        name_interface = args[2].split(':')
        device = simulator.computers[name_interface[0]]
        device.mac_addresses[address] = mac_address
        if len(device.mac_addresses) == 1:
            device.mac_address = mac_address
            device.first_key_mac_addresses = next(iter(device.mac_addresses))
        
class IP(Instruction):
    
    def execute(self, simulator, args):
        
        name_interface = args[2].split(':')
        name = name_interface[0]
        device = simulator.computers[name]
        if device is None:
            device = simulator.routers[name]
        
        bin_ip = simulator.get_bin_str(args[3])
        ip_address = IPAddress(bin_ip)
        
        bin_mask = simulator.get_bin_str(args[4])
        mask_address = SubnetworkMask(bin_mask)
        
        device.ip_mask_addresses[ip_address.address] = (ip_address, mask_address)
        
        if len(device.ip_mask_addresses) == 1:
            device.first_key_ip_mask_addresses = next(iter(device.ip_mask_addresses))
        
        subnetwork_address = device.subnetwork_address()
        
        subnetwork = None
        if not simulator.subnetworks.keys().__contains__(subnetwork_address):
            subnetwork = Subnetwork(subnetwork_address)
            simulator.subnetworks[subnetwork_address] = subnetwork
        else :
            subnetwork = simulator.subnetworks[subnetwork_address]
        
        subnetwork.devices[device.name] = device
        simulator.ip_dictionary[ip_address.address] = device
         
class SendFrame(Instruction):
    
    def execute(self, simulator, args):
        computer_name = args[2]
        
        target_mac = bin(int(args[3], 16))[2:].zfill(16)
        source_mac = bin(int(simulator.computers[computer_name].mac_address.address, 16))[2:].zfill(16)
        data_size = bin(int(len(args[4])/4))[2:].zfill(8)
        
        data = bin(int(args[4], 16))[2:].zfill(len(args[4]) * 4)
        
        
        v_data = simulator.bug_catcher.calculate(data)
        v_data_size = bin(int(len(v_data)))[2:].zfill(8)
        
        frame = Frame(target_mac, source_mac, data_size, v_data_size, data, v_data)
        
        transmission_data = ""
        for i in range(len(data)):
            
            transmission_data += data[i]
            
            simulator.computers[computer_name].write_txt(int(time() - simulator.start), simulator.computers[computer_name].ports[0], "send_frame", data[i], "ok")
            
            initial_time = time()
            queue_bfs = [simulator.computers[computer_name].ports[0]]
            while len(queue_bfs) > 0:
                current_port : Port = queue_bfs.pop(0)
                if current_port.cable == None:
                    continue
                current_cable : DuplexCable = current_port.cable
                
                # Selecting cable from duplex cable
                if current_cable.cable_1.port_1.name == current_port.name:
                    current_cable = current_cable.cable_1
                else :
                    current_cable = current_cable.cable_2
                
                current_cable.data = data[i]
                
                destination_port : Port = current_cable.port_2
                if destination_port == None:
                    continue
                
                # Saving mac addresses in switches
                if type(current_port.device) is Computer and type(destination_port.device) is Switch:
                    destination_port.device.mac_addresses[current_port.device.mac_address.address] = current_port.device.mac_address
                elif type(destination_port.device) is Computer and type(current_port.device) is Switch:
                    current_port.device.mac_addresses[destination_port.device.mac_address.address] = destination_port.device.mac_address
                    
                    
                if type(destination_port.device) is Computer:
                    if destination_port.device.mac_address.address == args[3]:
                        destination_port.device.write_txt(int(time() - simulator.start), destination_port, "receive_frame", transmission_data[i], "ok")
                        if i == len(data) - 1:
                            is_corrupt = simulator.bug_catcher.is_corrupted(frame.v_data, transmission_data)
                            destination_port.device.write_data_txt(int(time() - simulator.start), destination_port.device.name, frame.source_mac, hex(int(transmission_data, 2)), is_corrupt)
                        break
                    if args[3] == "FFFF":
                        destination_port.device.write_txt(int(time() - simulator.start), destination_port, "receive_frame", transmission_data[i], "ok")
                        if i == len(data) - 1:
                            is_corrupt = simulator.bug_catcher.is_corrupted(frame.v_data, transmission_data)
                            destination_port.device.write_data_txt(int(time() - simulator.start), destination_port.device.name, frame.source_mac, hex(int(transmission_data, 2)), is_corrupt)
                            
                
                
                for j in range(len(destination_port.device.ports)):
                    if destination_port.device.ports[j].name == destination_port.name:
                        continue
                    queue_bfs.append(destination_port.device.ports[j])
            sleep(simulator.signal_time - (time() - initial_time))
            

class Send(Instruction):
    
    def execute(self, simulator, args):
        computer_name = args[2]
        data = args[3]
        for i in range(len(data)):
            initial_time = time()
            queue_bfs = [simulator.computers[computer_name].ports[0]]
            while len(queue_bfs) > 0:
                current_port : Port = queue_bfs.pop(0)
                current_port.device.write_txt(int(time() - simulator.start), current_port, "send", data[i], "ok")
                if current_port.cable == None:
                    continue
                current_cable : DuplexCable = current_port.cable
                
                # Selecting cable from duplex cable
                if current_cable.cable_1.port_1.name == current_port.name:
                    current_cable = current_cable.cable_1
                else :
                    current_cable = current_cable.cable_2
                
                current_cable.data = data[i]
                
                destination_port : Port = current_cable.port_2
                if destination_port == None:
                    continue
                
                # Saving mac addresses in switches
                if type(current_port.device) is Computer and type(destination_port.device) is Switch:
                    destination_port.device.mac_addresses[current_port.device.mac_address.address] = current_port.device.mac_address
                elif type(destination_port.device) is Computer and type(current_port.device) is Switch:
                    current_port.device.mac_addresses[destination_port.device.mac_address.address] = destination_port.device.mac_address
                
                destination_port.device.write_txt(int(time() - simulator.start), destination_port, "receive", data[i], "ok")
                if type(destination_port.device) is Computer and i == len(data) - 1:
                    destination_port.device.write_data_txt(int(time() - simulator.start), destination_port.name, bin(int(simulator.computers[computer_name].mac_address.address, 16))[2:].zfill(16), hex(int(data, 2)), False)
                
                for j in range(len(destination_port.device.ports)):
                    if destination_port.device.ports[j].name == destination_port.name:
                        continue
                    queue_bfs.append(destination_port.device.ports[j])
            sleep(simulator.signal_time - (time() - initial_time))
            
class SendPacket(Instruction):
    
    def execute(self, simulator, args):
        
        host = simulator.computers[args[2]]
        source_ip = host.ip_mask_addresses[host.first_key_ip_mask_addresses][0]
        target_ip = simulator.get_bin_str(args[3])
        target_ip = simulator.ip_dictionary[target_ip].ip_mask_addresses[target_ip][0]
        
        payload_size = bin(int(len(args[4])/2))[2:].zfill(8)
        payload_data = bin(int(args[4], 16))[2:].zfill(len(args[4]) * 4)
        
        ip_packet = IPPacket(target_ip, source_ip, payload_size, payload_data)
        
        self.send(simulator, ip_packet, host)
        
    
    def send(self, simulator, ip_packet, host):
        
        target_ip = ip_packet.target_ip
        source_ip = ip_packet.source_ip
        
        destination_mac = ""
        
        if not host.contains_ip(target_ip):
            arp = ARP()
            destination_mac = arp.execute(simulator, host.mac_addresses[host.first_key_mac_addresses], target_ip)
        else : 
            destination_host = simulator.ip_dictionary[target_ip]
            destination_mac = destination_host.mac_addresses[destination_host.first_key_mac_addresses]
        
        device_with_ip = host.routing(ip_packet, simulator)
        
        #device from router routing
        if device_with_ip[0] is not None:
            icmp = ICMP()
            icmp_packet = icmp.execute(simulator, source_ip, device_with_ip[0].ip_mask_addresses[device_with_ip[0].first_key_ip_mask_addresses][0], bin(3)[2:].zfill(8))
            
            self.send(simulator, icmp_packet, device_with_ip[0])
        
        #device from host routing
        if device_with_ip[1] is not None:
            icmp = ICMP()
            icmp_packet = icmp.execute(simulator, source_ip, device_with_ip[1].ip_mask_addresses[device_with_ip[1].first_key_ip_mask_addresses][0], bin(0)[2:].zfill(8))
            
            self.send(simulator, icmp_packet, device_with_ip[1])
            
class Ping(Instruction):
    
    def execute(self, simulator, args):
        icmp = ICMP()
        host = simulator.computers[args[2]]
        ping_icmp_packet = icmp.execute(simulator, args[3], host.ip_mask_addresses[host.first_key_ip_mask_addresses][0], "00001000")
        send_packet = SendPacket() 
        for i in range(4):
            initial_time = time()
            send_packet.send(simulator, ping_icmp_packet, host)
            sleep(100/1000 - (time() - initial_time))
            
class Route(Instruction):
    def __init__(self):
        self.route_instructions = {"reset" : RouteReset(), "add" : RouteAdd(), "delete" : RouteDelete()}
    
    def execute(self, simulator, args):
        route_instruction = self.route_instructions[args[2]]
        route_instruction.execute(simulator, args)

class RouteReset(Instruction):
    
    def execute(self, simulator, args):
        simulator.routers[args[3]].routes_table.clear()

class RouteAdd(Instruction):
    
    def execute(self, simulator, args):
        simulator.routers[args[3]].insert_route(Route(args[4], args[5], args[6], args[7]))
        
class RouteDelete(Instruction):
    
    def execute(self, simulator, args):
        
        # Verifies the correct use of instruction RouteDelete
        if len(args) != 8: 
            return
        
        router : Router = simulator.routers[args[3]]
        for route in router.routes_table:
            if args[4] == route.target_ip and args[5] == route.route_mask and args[6] == route.gateway_ip and args[7] == route.interface:
                router.routes_table.remove(route)
        