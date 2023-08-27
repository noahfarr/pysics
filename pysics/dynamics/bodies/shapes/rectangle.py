import numpy as np

from .shape import Shape
from collision.aabb import AABB

class Rectangle(Shape):

    def __init__(self, mass: float, width: float, height: float):
        self.width = width
        self.height = height
        self.center_of_mass = self.compute_center_of_mass()
        super().__init__(mass)

    def compute_inertia(self, mass: float):
        return mass * (self.width ** 2 + self.height ** 2) / 12.0
    
    def compute_center_of_mass(self):
        return np.array([self.width / 2.0, self.height / 2.0])
    
    def draw(self, renderer, body):
        renderer.draw_rectangle(body)