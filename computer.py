from port import Port


class Computer:
    def __init__(self, name):
        self.name = name
        self.port = Port(name + "_" + str(1))
