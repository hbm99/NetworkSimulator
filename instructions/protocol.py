
from abc import ABC, abstractmethod
from time import time
from network_components.device_utils import Frame


class Protocol(ABC):
    
    @abstractmethod
    def execute(self, simulator):
        pass
    
class ARP(Protocol):
    
    def execute(self, simulator, source_mac : str, target_ip : str):
        
        target_mac = bin(int("FFFF", 16))[2:].zfill(16)
        source_mac = bin(int(source_mac))[2:].zfill(16)
        data_size = bin(8)[2:].zfill(8)
        data = ''.join(format(ord(x), 'b') for x in "ARPQ") + target_ip
        v_data = ""
        v_data_size = bin(int(len(v_data)))[2:].zfill(8)
        
        query_frame = Frame(target_mac, source_mac, data_size, v_data_size, data, v_data)
        
        mac_from_target_ip = self.send_special_frame(query_frame, simulator)
        
        target_mac = source_mac
        source_mac = mac_from_target_ip
        
        data = ''.join(format(ord(x), 'b') for x in "ARPR") + target_ip
        
        response_frame = Frame(target_mac, source_mac, data_size, v_data_size, data, v_data)
        
        self.send_special_frame(response_frame, simulator) #¿podrá ejecutarse como void aunque retorne un valor? pendiente de testear
        
        return mac_from_target_ip
        
    def send_special_frame(frame : Frame, simulator):
        
        target_ip = frame.data[32:]
        mac_from_target_ip = ""
        
        for computer_value in simulator.computers.values():
            if computer_value.mac_addresses.__contains__(frame.target_mac) or frame.target_mac == "1" * 32:
                computer_value.write_payload_txt(computer_value.name, int(time() - simulator.start), target_ip, frame.data)
            for ip_mask in computer_value.ip_mask_addresses:
                if ip_mask[0].address == target_ip:
                    mac_from_target_ip = computer_value.mac_addresses[next(iter(computer_value.mac_addresses))]
    
        return mac_from_target_ip