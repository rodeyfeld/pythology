from __future__ import annotations
from abc import ABC, abstractmethod
import augury.models


class Seeker(ABC):

    @abstractmethod
    def seek(self, study) -> "Dream":
        ...
    @abstractmethod
    def poll(self, study) -> "Dream":
        ...


    