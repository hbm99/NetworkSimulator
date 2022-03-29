from instructions.instruction import Instruction


class Disconnect(Instruction):
    
    def execute(self, simulator, args):
        port = simulator.find_port(args[2])
        cable = port.cable
        if cable.port_1.name == port.name:
            cable.port_1 = None
        else : 
            cable.port_2 = None
        port.cable = None
        
        
    