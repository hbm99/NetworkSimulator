
class Frame:
    def __init__(self, target_mac : str, source_mac : str, data_size : str, v_data_size : str, data : str, v_data : str):
        self.target_mac = target_mac
        self.source_mac = source_mac
        self.data_size = data_size
        self.v_data_size = v_data_size
        self.data = data
        self.v_data = v_data
        