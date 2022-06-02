
from abc import ABC, abstractmethod
from time import time
from typing import Dict
from network_components.device_utils import Frame, IPPacket


class Protocol(ABC):
    
    @abstractmethod
    def execute(self, simulator):
        pass
    
class ARP(Protocol):
    
    def execute(self, simulator, source_mac : str, target_ip : str):
        
        target_mac = bin(int("FFFF", 16))[2:].zfill(16)
        source_mac = bin(int(source_mac.address))[2:].zfill(16)
        data_size = bin(8)[2:].zfill(8)
        data = ''.join(format(ord(x), 'b') for x in "ARPQ") + target_ip.address
        v_data = ""
        v_data_size = bin(int(len(v_data)))[2:].zfill(8)
        
        query_frame = Frame(target_mac, source_mac, data_size, v_data_size, data, v_data)
        
        mac_from_target_ip = self.send_special_frame(query_frame, simulator)
        
        target_mac = source_mac
        source_mac = mac_from_target_ip
        
        data = ''.join(format(ord(x), 'b') for x in "ARPR") + target_ip.address
        
        response_frame = Frame(target_mac, source_mac, data_size, v_data_size, data, v_data)
        
        self.send_special_frame(response_frame, simulator) #¿podrá ejecutarse como void aunque retorne un valor? pendiente de testear
        
        return mac_from_target_ip
        
    def send_special_frame(self, frame : Frame, simulator):
        
        target_ip = frame.data[32:]
        mac_from_target_ip = ""
        
        for computer_value in simulator.computers.values():
            if computer_value.mac_addresses.__contains__(frame.target_mac) or frame.target_mac == "1" * 32:
                computer_value.write_payload_txt(computer_value.name, int(time() - simulator.start), target_ip, frame.data)
            for ip_mask in computer_value.ip_mask_addresses.values():
                if ip_mask[0].address == target_ip:
                    mac_from_target_ip = computer_value.mac_addresses[next(iter(computer_value.mac_addresses))]
    
        return mac_from_target_ip
    
class ICMP(Protocol):
    def __init__(self):
        self.control_message = {0 : "echo reply", 3 : "destination host unreachable", 8 : "echo request", 11 : "time exceeded"}
    
    def execute(self, simulator, destination_ip, source_ip, payload_data, ttl = "0" * 8):
        return IPPacket(destination_ip, source_ip, "0" * 7 + "1", payload_data, ttl, "0" * 7 + "1")