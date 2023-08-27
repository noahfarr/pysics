import numpy as np
from .shape import Shape
from collision.aabb import AABB

class Circle(Shape):

    def __init__(self, mass: float, radius: float):
        self.radius = radius
        self.center_of_mass = self.compute_center_of_mass()
        super().__init__(mass)

    def compute_inertia(self, mass: float):
        return 0.5 * mass * self.radius ** 2
    
    def compute_center_of_mass(self):
        # For a uniform circle, the center of mass is at its center
        return np.array([0.0, 0.0])

    def draw(self, renderer, body):
        renderer.draw_circle(body)
