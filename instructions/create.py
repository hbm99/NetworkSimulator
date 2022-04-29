from instructions.instruction import Instruction
from network_components.computer.computer import Computer
from network_components.hub import Hub
from network_components.switch import Switch


class Create(Instruction):
    
    def execute(self, simulator, args):
        if args[2] == "hub":
            hub = Hub(args[3], args[4])
            simulator.hubs[args[3]] = hub
        elif args[2] == "host":
            computer = Computer(args[3])
            simulator.computers[args[3]] = computer
        elif args[2] == "switch":
            switch = Switch(args[3], args[4])
            simulator.switches[args[3]] = switch