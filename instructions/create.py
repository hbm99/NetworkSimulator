from instructions.instruction import Instruction
from simulator import computers, hubs
from network_components.computer.computer import Computer
from network_components.hub import Hub


class Create(Instruction):
    
    def execute(self, args):
        if args[2] == "hub":
            hubs.append(Hub(args[3], args[4]))
        else :
            computers.append(Computer(args(3)))