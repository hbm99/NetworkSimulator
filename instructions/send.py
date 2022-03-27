from time import time
from tracemalloc import start
from instructions.instruction import Instruction
from network_components.cable import Cable
from network_components.port import Port
from simulator import Simulator

class Send(Instruction):
    
    
    def execute(self, args):
        computer = args[2]
        data = args[3]
        for i in range(len(data)):
            queue_bfs = [computer.port]
            while len(queue_bfs) > 0:
               current_port : Port = queue_bfs.pop(0)
               if current_port.cable == None:
                   continue
               current_port.device.write(int(time.time() - Simulator.start_time), computer.port.name, "send", data[i], "ok")
               current_cable : Cable = current_port.cable
               current_cable.data = data[i]
               destination_port : Port = current_cable.port_1 if current_cable.port_1.name != current_port.name else current_cable.port_2
               destination_port.device.write(int(time.time() - Simulator.start_time), destination_port.name, "receive", data[i], "ok")
               for j in range(len(destination_port.device.ports)):
                   if destination_port.device.ports[j].name == destination_port.name:
                       continue
                   queue_bfs.append(destination_port.device.ports[j])
                   
