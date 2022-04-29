from network_components.device import Device
from network_components.port import Port


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
