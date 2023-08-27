import numpy as np

from dynamics.bodies.body import Body
from collision.broad_phase.sort_and_sweep import sort_and_sweep

class World:

    def __init__(self, gravity: np.ndarray):
        self.gravity = gravity
        self.bodies = list()
        self.renderer = None

    def set_renderer(self, renderer):
        self.renderer = renderer

    def add_body(self, body: Body):
        self.bodies.append(body)

    def remove_body(self, body: Body):
        self.bodies.remove(body)

    def apply_gravity(self, body: Body):
        body.apply_force(self.gravity * body.shape.mass)

    def apply_forces(self, body: Body):
        self.apply_gravity(body)

    def update(self, dt: float):
        for _, body in enumerate(self.bodies):
            self.apply_forces(body)
            body.update(dt)
        overlapping_bodies = sort_and_sweep(self.bodies, 0)
        for body1, body2 in overlapping_bodies:
            if body1.intersects(body2):
                print("Collision detected")

        if self.renderer is not None:
            self.renderer.render(self.bodies)

