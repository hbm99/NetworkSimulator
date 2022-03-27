from network_components.device import Device
from network_components.port import Port


class Hub(Device):
    def __init__(self, name, ports_count):
        self.name = name
        self.ports = self.create_ports(self, name, int(ports_count))
    
    def create_ports(self, name, ports_count):
        ports = []
        for i in range(ports_count):
            ports[i] = Port(name + "_" + str(i), self)
        return ports
