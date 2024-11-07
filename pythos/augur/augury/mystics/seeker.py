from abc import ABC, abstractmethod

class Seeker(ABC):

    @abstractmethod
    def seek(self, study) -> "Dream": # type: ignore
        ...
    @abstractmethod
    def poll(self, study) -> "Dream": # type: ignore
        ...
