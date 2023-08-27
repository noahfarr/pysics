from abc import ABC, abstractmethod
import numpy as np

class BoundingVolume(ABC):

    @abstractmethod
    def contains(self, point) -> bool:
        pass

    @abstractmethod
    def intersects(self, other) -> bool:
        pass

    @abstractmethod
    def get_extend_along_axis(self, axis: int):
        pass
