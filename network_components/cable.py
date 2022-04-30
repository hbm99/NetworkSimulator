from network_components.data import Data


class Cable:
    def __init__(self, data, port_1, port_2):
        self.data = data
        self.port_1 = port_1
        self.port_2 = port_2


class DuplexCable:
    def __init__(self, port_1, port_2):
        self.cable_1 = Cable(Data(None), port_1, port_2)
        self.cable_2 = Cable(Data(None), port_2, port_1)
        
        
        