from abc import ABC, abstractmethod

class BugCatcher(ABC):
    
    @abstractmethod
    def calculate(self, data):
        pass
    
    @abstractmethod
    def is_corrupted(self, data_1, data_2):
        pass