from instructions.instruction import Instruction


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
        
        
    