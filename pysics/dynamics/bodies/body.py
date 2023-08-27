import numpy as np
from abc import ABC, abstractmethod

class Body(ABC):
    
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray):
        self.mass = mass
        assert position.shape == (2,), "Position must be a 2D vector"
        assert velocity.shape == (2,), "Velocity must be a 2D vector"
        assert acceleration.shape == (2,), "Acceleration must be a 2D vector"
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.force = np.array([0.0, 0.0])

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def apply_force(self, force: np.ndarray):
        pass

    @abstractmethod
    def reset_force(self):
        pass

    @abstractmethod
    def apply_torque(self, application_point: np.ndarray = None):
        pass

    @abstractmethod
    def reset_torque(self):
        pass

    @abstractmethod
    def get_bounding_volume(self):
        pass

    @abstractmethod
    def intersects(self, other):
        pass