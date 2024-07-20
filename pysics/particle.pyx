import numpy as np
cimport numpy as cnp
cnp.import_array()


cdef class Particle:

    cdef double mass
    cdef double radius
    cdef cnp.ndarray force
    cdef cnp.ndarray position
    cdef cnp.ndarray velocity
    cdef cnp.ndarray acceleration

    def __init__(
        self,
        double mass,
        double radius,
        cnp.ndarray force,
        cnp.ndarray position,
        cnp.ndarray velocity,
        cnp.ndarray acceleration,
    ) -> None:
        self.mass = mass
        self.radius = radius
        self.force = force
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self, double dt, double gravity):
        self.acceleration = self.force / self.mass
        self.velocity += dt * self.acceleration
        self.position += dt * self.velocity
        self.force = np.array([0.0, gravity])

    cdef void apply_force(self, cnp.ndarray force):
        self.force += force

    def distance_to(self, Particle other):
        cdef double distance
        distance = np.linalg.norm(other.position - self.position).item()
        return distance

    def collides_with(self, Particle other):
        cdef double distance
        distance = self.distance_to(other)
        return distance <= (self.radius + other.radius)

    @property
    def mass(self):
        return self.mass

    @mass.setter
    def mass(self, value):
        self.mass = value

    @property
    def radius(self):
        return self.radius

    @radius.setter
    def radius(self, value):
        self.radius = value

    @property
    def force(self):
        return self.force

    @force.setter
    def force(self, value):
        self.force = value

    @property
    def position(self):
        return self.position

    @position.setter
    def position(self, value):
        self.position = value

    @property
    def velocity(self):
        return self.velocity

    @velocity.setter
    def velocity(self, value):
        self.velocity = value

    @property
    def acceleration(self):
        return self.acceleration

    @acceleration.setter
    def acceleration(self, value):
        self.acceleration = value
