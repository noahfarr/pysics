# particle.pyx
import numpy as np
cimport numpy as cnp
cnp.import_array()

cdef class Particle:
    def __init__(self, double mass, double radius, cnp.ndarray force, cnp.ndarray position, cnp.ndarray velocity, cnp.ndarray acceleration) -> None:
        self.mass = mass
        self.radius = radius
        self.force = force
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    cdef void update(self, double dt, double gravity):
        self.acceleration = self.force / self.mass
        self.velocity += dt * self.acceleration
        self.position += dt * self.velocity

        self.force = np.array([0.0, gravity])
