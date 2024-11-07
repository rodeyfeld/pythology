from abc import ABC, abstractmethod

class Diviner(ABC):

    @abstractmethod
    def divine(self, dream):
        ...
        