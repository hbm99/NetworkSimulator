from instructions.instruction import Instruction

class Mac(Instruction):
    
    def execute(self, simulator, args):
        simulator.computers[args[2]].mac_address.address = args[3]
        