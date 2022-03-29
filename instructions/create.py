from instructions.instruction import Instruction
from network_components.computer.computer import Computer
from network_components.hub import Hub


class Create(Instruction):
    
    def execute(self, simulator, args):
        if args[2] == "hub":
            hub = Hub(args[3], args[4])
            # simulator.add_device(hub)
            simulator.hubs.append(hub)
        elif args[2] == "host":
            computer = Computer(args[3])
            # simulator.add_device(computer)
            simulator.computers.append(computer)