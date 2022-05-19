

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
