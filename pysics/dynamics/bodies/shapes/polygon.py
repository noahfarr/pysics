import numpy as np
from .shape import Shape
from collision.aabb import AABB

class Polygon(Shape):

    def __init__(self, mass: float, radius, num_vertices):
        self.vertices = self.get_vertices(radius, num_vertices)
        self.center_of_mass = self.compute_center_of_mass()
        super().__init__(mass)

    def get_vertices(self, radius, num_vertices):
        vertices = np.empty((num_vertices, 2))
        for i in range(num_vertices):
            angle = np.radians(float(i) / num_vertices * 360.0)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            vertices[i] = np.array([x, y])
        return vertices

    def compute_inertia(self, mass: float):
        vertices = self.vertices
        n = len(vertices)
        inertia = 0.0

        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]  # Next vertex, loop back to 0 at the end

            factor = (x1 * y2) - (x2 * y1)
            term = (x1**2 + x2**2 + y1**2 + y2**2)

            inertia += factor * term

        inertia *= mass / 12.0

        # Check for zero or negative inertia, which could lead to problems
        assert inertia > 0.0, "Inertia must be positive"

        return inertia

    def compute_center_of_mass(self):
        # For a uniform, convex polygon, the center of mass can be approximated as the centroid,
        # which is the average of its vertices.
        return np.mean(self.vertices, axis=0)

    def draw(self, renderer, body):
        renderer.draw_polygon(body)
