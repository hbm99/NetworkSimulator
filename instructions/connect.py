from instructions.instruction import Instruction
from network_components.cable import Cable
from network_components.computer.data import Data

class Connect(Instruction):
    
    def execute(self, simulator, args):
        port_1 = simulator.find_port(args[2])
        port_2 = simulator.find_port(args[3])
        wire = Cable(Data(None), port_1, port_2)
        port_1.cable, port_2.cable = wire
        
    
        