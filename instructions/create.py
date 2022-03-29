from instructions.instruction import Instruction
from main import simulator
from network_components.computer.computer import Computer
from network_components.hub import Hub


class Create(Instruction):
    
    def execute(self, args):
        if args[2] == "hub":
            simulator.hubs.append(Hub(args[3], args[4]))
        else :
            simulator.computers.append(Computer(args(3)))