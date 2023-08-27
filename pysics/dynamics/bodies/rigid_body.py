import numpy as np

from dynamics.bodies.body import Body
from dynamics.bodies.shapes.shape import Shape

class RigidBody(Body):

    def __init__(self, position: np.ndarray, linear_velocity: np.ndarray, angle: float, angular_velocity: float, shape: Shape, bounding_volume_factory):
        self.position = position
        self.linear_velocity = linear_velocity
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.force = np.zeros(2)
        self.torque = 0.0
        self.shape = shape
        self.bounding_volume_factory = bounding_volume_factory
        self.bounding_volume = bounding_volume_factory(self.position, self.angle, self.shape)


    def update(self, dt: float):
        self.linear_acceleration = self.force / self.shape.mass
        self.linear_velocity += self.linear_acceleration * dt
        self.position += self.linear_velocity * dt
        self.angular_acceleration = self.torque / self.shape.inertia
        self.angular_velocity += self.angular_acceleration * dt
        self.angle += self.angular_velocity * dt
        self.angle = self.angle % (2 * np.pi)
        self.update_bounding_volume()
        self.reset_force()
        self.reset_torque()

    def update_bounding_volume(self):
        self.bounding_volume = self.bounding_volume_factory(self.position, self.angle, self.shape)

    def apply_force(self, force: np.ndarray):
        self.force += force

    def apply_torque(self, application_point: np.ndarray = None):
        if application_point is None:
            application_point = self.shape.center_of_mass
        self.torque += np.cross(application_point, self.force)

    def reset_force(self):
        self.force = np.array([0.0, 0.0])

    def reset_torque(self):
        self.torque = 0.0

    def get_bounding_volume(self):
        return self.bounding_volume
    
    def intersects(self, other):
        return self.bounding_volume.intersects(other.bounding_volume)