import numpy as np

from .bounding_volume import BoundingVolume

class AABB(BoundingVolume):

    def __init__(self, min: np.ndarray, max: np.ndarray):
        self.min = min
        self.max = max

    def contains(self, point: np.ndarray) -> bool:
        return np.all(point >= self.min) and np.all(point <= self.max)

    def intersects(self, other) -> bool:
        return np.all(self.min <= other.max) and np.all(self.max >= other.min)

    def get_extend_along_axis(self, axis: int) -> float:
        return self.min[axis], self.max[axis]