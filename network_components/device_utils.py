

class Data:
    def __init__(self, str_data):
        self.str_data = str_data
        
class Cable:
    def __init__(self, data, port_1, port_2):
        self.data = data
        self.port_1 = port_1
        self.port_2 = port_2

class DuplexCable:
    def __init__(self, port_1, port_2):
        self.cable_1 = Cable(Data(None), port_1, port_2)
        self.cable_2 = Cable(Data(None), port_2, port_1)
        
class Port:
    def __init__(self, name, device):
        self.name = name
        self.cable = None
        self.device = device

class Frame:
    def __init__(self, target_mac : str, source_mac : str, data_size : str, v_data_size : str, data : str, v_data : str):
        self.target_mac = target_mac
        self.source_mac = source_mac
        self.data_size = data_size
        self.v_data_size = v_data_size
        self.data = data
        self.v_data = v_data

class MacAddress:
    def __init__(self, address : str):
        self.address = address
        
class IPAddress:
    def __init__(self, address : str):
        self.address = address

class SubnetworkMask:
    def __init__(self, address : str):
        self.address = address
        
class Subnetwork:
    def __init__(self, address : str):
        self.address = address
        self.devices = {}
        
class Route:
    def __init__(self, destination_ip : str, route_mask : str, gateway_ip: str, interface : int):
        self.destination_ip = destination_ip
        self.route_mask = route_mask
        self.gateway_ip = gateway_ip
        self.interface = interface

class IPPacket:
    def __init__(self, destination_ip, source_ip, payload_size, payload_data, time_to_live = "0" * 8, protocol = "0" * 8):
        self.destination_ip = destination_ip
        self.source_ip = source_ip
        self.ttl = time_to_live
        self.protocol = protocol
        self.payload_size = payload_size
        self.payload_data = payload_data
        