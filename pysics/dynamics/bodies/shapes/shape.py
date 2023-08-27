from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, mass: float):
        self.mass = mass
        self.inertia = self.compute_inertia(self.mass)

    @abstractmethod
    def compute_inertia(self, mass: float):
        pass

    @abstractmethod
    def compute_center_of_mass(self):
        pass

    @abstractmethod
    def draw(self, renderer, body):
        pass