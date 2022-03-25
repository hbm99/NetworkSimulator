from port import Port


class Hub:
    def __init__(self, name, ports_count):
        self.name = name
        self.ports = self.create_ports(name, ports_count)
    
    def create_ports(name, ports_count):
        ports = []
        for i in range(ports_count):
            ports[i] = Port(name + "_" + str(i))
        return ports
