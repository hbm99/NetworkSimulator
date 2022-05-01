from time import time, sleep
from instructions.instruction import Instruction
from network_components.cable import DuplexCable
from network_components.computer import Computer
from network_components.mac_address import MacAddress
from network_components.port import Port
from network_components.switch import Switch

class Send(Instruction):
    
    def execute(self, simulator, args):
        computer_name = args[2]
        data = args[3]
        for i in range(len(data)):
            initial_time = time()
            queue_bfs = [simulator.computers[computer_name].ports[0]]
            while len(queue_bfs) > 0:
                current_port : Port = queue_bfs.pop(0)
                current_port.device.write_txt(int(time() - simulator.start), current_port, "send", data[i], "ok")
                if current_port.cable == None:
                    continue
                current_cable : DuplexCable = current_port.cable
                
                # Selecting cable from duplex cable
                if current_cable.cable_1.port_1.name == current_port.name:
                    current_cable = current_cable.cable_1
                else :
                    current_cable = current_cable.cable_2
                
                current_cable.data = data[i]
                
                destination_port : Port = current_cable.port_2
                if destination_port == None:
                    continue
                
                # Saving mac addresses in switches
                if type(current_port.device) is Computer and type(destination_port.device) is Switch:
                    destination_port.device.mac_addresses[current_port.device.mac_address.address] = current_port.device.mac_address
                elif type(destination_port.device) is Computer and type(current_port.device) is Switch:
                    current_port.device.mac_addresses[destination_port.device.mac_address.address] = destination_port.device.mac_address
                
                destination_port.device.write_txt(int(time() - simulator.start), destination_port, "receive", data[i], "ok")
                if type(destination_port.device) is Computer and i == len(data) - 1:
                    destination_port.device.write_data_txt(int(time() - simulator.start), destination_port.name, bin(int(simulator.computers[computer_name].mac_address.address, 16))[2:].zfill(16), hex(int(data, 2)), False)
                
                for j in range(len(destination_port.device.ports)):
                    if destination_port.device.ports[j].name == destination_port.name:
                        continue
                    queue_bfs.append(destination_port.device.ports[j])
            sleep(10/1000 - (time() - initial_time))

