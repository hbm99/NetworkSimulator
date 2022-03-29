from time import time
from instructions.instruction import Instruction
from network_components.cable import Cable
from network_components.port import Port

class Send(Instruction):
    
    def execute(self, simulator, args):
        computer = args[2]
        data = args[3]
        for i in range(len(data)):
            initial_time = time() * 1000
            while time() * 1000 - initial_time <= simulator.signal_time:
                queue_bfs = [computer.ports[0]]
                while len(queue_bfs) > 0:
                    current_port : Port = queue_bfs.pop(0)
                    if current_port.cable == None:
                        continue
                    current_port.device.write(int(time() - simulator.start), computer.port, "send", data[i], "ok")
                    current_cable : Cable = current_port.cable
                    current_cable.data = data[i]
                    destination_port : Port = current_cable.port_1 if current_cable.port_1.name != current_port.name else current_cable.port_2
                    destination_port.device.write(int(time() - simulator.start), destination_port, "receive", data[i], "ok")
                    for j in range(len(destination_port.device.ports)):
                        if destination_port.device.ports[j].name == destination_port.name:
                            continue
                        queue_bfs.append(destination_port.device.ports[j])
