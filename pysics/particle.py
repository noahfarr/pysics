import numpy as np


class Particle:

    mass: float
    radius: float
    force: np.ndarray
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    radius: float

    def __init__(
        self,
        force: np.ndarray,
        position: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray,
        mass: float | None = None,
        radius: float | None = None,
    ) -> None:
        self.mass = mass or 1.0
        self.radius = radius or 10.0
        self.force = force
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(
        self, dt: float, gravity: float, MAX_VELOCITY: float, VELOCITY_DAMP: float
    ) -> None:
        self.acceleration = self.force / self.mass
        self.velocity += dt * self.acceleration

        self.position += dt * self.velocity
        self.force = np.array([0.0, gravity])

    def apply_force(self, force: np.ndarray) -> None:
        self.force += force

    def distance_to(self, other) -> float:
        distance = np.linalg.norm(other.position - self.position).item()
        return distance

    def collides_with(self, other) -> bool:
        distance = self.distance_to(other)
        return distance <= (self.radius + other.radius)

    def resolve_collision(self, other) -> None:
        direction = other.position - self.position
        distance = np.linalg.norm(direction).item()

        normalized_direction = direction / distance
        penetration_depth = (self.radius + other.radius) - distance
        movement = normalized_direction * (penetration_depth / 2)

        self.position -= movement
