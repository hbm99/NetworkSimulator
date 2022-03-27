from network_components.device import Device
from network_components.port import Port


class Computer(Device):
    def __init__(self, name):
        super().__init__(name)
        self.ports = [Port(name + "_" + str(1), self)]
