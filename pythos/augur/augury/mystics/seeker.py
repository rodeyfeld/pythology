from abc import ABC, abstractmethod

class Seeker(ABC):

    @abstractmethod
    def seek(self, study):
        ...
    @abstractmethod
    def poll(self, study):
        ...
    