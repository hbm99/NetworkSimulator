from abc import ABC, abstractmethod

class BugCatcher(ABC):
    
    @abstractmethod
    def calculate(self, data):
        pass
    
    @abstractmethod
    def is_corrupted(self, data_1, data_2):
        pass
    
class VerificationSum(BugCatcher):
    
    def calculate(self, data : bin):
        str_data =  str(data)
        bin_chunks = [str_data[8*i:8*(i+1)] for i in range(len(str_data)//8)]
        ints = [int(x, 2) for x in bin_chunks]
        return bin(sum(ints))
    
    def is_corrupted(self, sum_data_1, data_2):
        return sum_data_1 != self.calculate(data_2)