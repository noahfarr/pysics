from time import sleep

import numpy as np
from tqdm import tqdm

from pysics.render import Renderer, RaylibRenderer
from pysics.particle import Particle


class Simulation:

    particles: list[Particle]
    dt: float
    renderer: Renderer

    WALL_DAMP: float

    def __init__(
        self,
        n_particles: int,
        dt: float,
        renderer: Renderer,
        gravity: float = -9.81,
        WALL_DAMP: float = 0.95,
        RESTITUTION: float = 0.95,
    ) -> None:
        self.renderer = renderer

        self.n_particles = n_particles
        self.particles = self.generate_particles(self.n_particles)

        self.dt = dt
        self.gravity = gravity
        self.WALL_DAMP = WALL_DAMP
        self.RESTITUTION = RESTITUTION

    def generate_particles(self, n_particles: int) -> list[Particle]:
        MIN_X, MIN_Y = 0, 0
        MAX_X, MAX_Y = self.renderer.size

        MIN_X_VEL, MIN_Y_VEL = 0, 0
        MAX_X_VEL, MAX_Y_VEL = 1000, 1000

        particles: list[Particle] = []
        for i in range(n_particles):
            x = np.random.uniform(MIN_X, MAX_X)
            y = np.random.uniform(MIN_Y, MAX_Y)

            x_vel = np.random.uniform(MIN_X_VEL, MAX_X_VEL)
            y_vel = np.random.uniform(MIN_Y_VEL, MAX_Y_VEL)

            vx = np.random.uniform
            particles.append(
                Particle(
                    force=np.array([0.0, 0.0]),
                    position=np.array([x, y]),
                    velocity=np.array([x_vel, y_vel]),
                    acceleration=np.array([0.0, 0.0]),
                )
            )
        return particles

    def simulate(self, total_timesteps: float, render: bool = False):

        for timestep in tqdm(np.arange(0.0, total_timesteps, self.dt)):
            self.step()

            collision_pairs = self.check_collision()
            self.resolve_collisions(collision_pairs)
            self.enforce_constraints()

            if render:
                self.renderer.render(self.particles)

    def apply_force(self, force: np.ndarray):
        for particle in self.particles:
            particle.apply_force(force)

    def step(self):
        for particle in self.particles:
            particle.update(self.dt, self.gravity)

    def check_collision(self) -> list[tuple[Particle, Particle]]:

        grid_size = 100
        grid = {}

        for particle in self.particles:
            key: tuple[int, int] = (
                particle.position[0] // grid_size,
                particle.position[1] // grid_size,
            )
            if key not in grid:
                grid[key] = []
            grid[key].append(particle)

        collision_pairs = []
        for cell_particles in grid.values():
            for i, particle in enumerate(cell_particles):
                for j in range(i + 1, len(cell_particles)):
                    other = cell_particles[j]
                    if particle.collides_with(other):
                        collision_pairs.append((particle, other))

        return collision_pairs

    def resolve_collisions(self, collision_pairs: list[tuple[Particle, Particle]]):
        for particle, other in collision_pairs:
            direction = other.position - particle.position
            distance = particle.distance_to(other)
            normal = direction / distance

            dv = other.velocity - particle.velocity

            dv_along_normal = dv.dot(normal)

            if dv_along_normal > 0:
                continue

            magnitude = -(1.0 + self.RESTITUTION) * dv_along_normal
            magnitude /= (1 / particle.mass) + (1 / other.mass)

            impulse = normal * magnitude
            particle.velocity -= (1 / particle.mass) * impulse
            other.velocity += (1 / other.mass) * impulse

    def enforce_constraints(self):

        for particle in self.particles:
            X_MIN = 0
            Y_MIN = 0
            X_MAX, Y_MAX = self.renderer.size

            x, y = particle.position
            if X_MIN >= (x - particle.radius):
                particle.position[0] = X_MIN + particle.radius
                particle.velocity[0] = -self.WALL_DAMP * particle.velocity[0]

            if X_MAX <= (x + particle.radius):
                particle.position[0] = X_MAX - particle.radius
                particle.velocity[0] = -self.WALL_DAMP * particle.velocity[0]

            if Y_MIN >= (y - particle.radius):
                particle.position[1] = Y_MIN + particle.radius
                particle.velocity[1] = -self.WALL_DAMP * particle.velocity[1]

            if Y_MAX <= (y + particle.radius):
                particle.position[1] = Y_MAX - particle.radius
                particle.velocity[1] = -self.WALL_DAMP * particle.velocity[1]
