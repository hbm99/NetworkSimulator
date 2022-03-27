from instructions.instruction import Instruction
from network_components.cable import Cable
from network_components.computer.data import Data

class Connect(Instruction):
    
    def execute(self, args):
        port_1 = self.find_port(args[2])
        port_2 = self.find_port(args[3])
        wire = Cable(Data(None), port_1, port_2)
        port_1.cable, port_2.cable = wire
        
    
        