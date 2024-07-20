import numpy as np
cimport numpy as cnp
cnp.import_array()

from tqdm import tqdm

from particle import Particle

cdef class Simulation:

    cdef cnp.ndarray particles
    cdef int n_particles
    cdef double gravity
    cdef double dt
    cdef renderer
    cdef double WALL_DAMP
    cdef double RESTITUTION

    def __init__(
        self,
        int n_particles,
        double dt,
        renderer,
        double gravity,
        double WALL_DAMP,
        double RESTITUTION,
    ) -> None:
        self.renderer = renderer

        self.n_particles = n_particles
        self.particles = self.generate_particles(self.n_particles)

        self.dt = dt
        self.gravity = gravity
        self.WALL_DAMP = WALL_DAMP
        self.RESTITUTION = RESTITUTION

    cdef cnp.ndarray generate_particles(self, int n_particles):
        cdef int MIN_X, MIN_Y, MAX_X, MAX_Y, MIN_X_VEL, MIN_Y_VEL, MAX_X_VEL, MAX_Y_VEL
        cdef double x, y, x_vel, y_vel
        cdef cnp.ndarray particles
        MIN_X = 0
        MIN_Y = 0
        MAX_X = self.renderer.size[0]
        MAX_Y = self.renderer.size[1]

        MIN_X_VEL = 0
        MIN_Y_VEL = 0
        MAX_X_VEL = 0
        MAX_Y_VEL = 0

        particles = np.empty(n_particles, dtype=object)
        for i in range(n_particles):
            x = np.random.uniform(MIN_X, MAX_X)
            y = np.random.uniform(MIN_Y, MAX_Y)

            x_vel = np.random.uniform(MIN_X_VEL, MAX_X_VEL)
            y_vel = np.random.uniform(MIN_Y_VEL, MAX_Y_VEL)

            particles[i] = Particle(1.0, 10.0, np.array([0.0, self.gravity]), np.array([x, y]), np.array([x_vel, y_vel]), np.array([0.0, 0.0]),)

        return particles

    def simulate(self, double total_timesteps, bint render):
        cdef list collision_pairs

        for timestep in tqdm(np.arange(0.0, total_timesteps, self.dt)):
            self.step()

            collision_pairs = self.check_collision()
            self.resolve_collisions(collision_pairs)
            self.enforce_constraints()

            if render:
                self.renderer.render(self.particles)

    cdef step(self):
        cdef particle
        for i in range(self.n_particles):
            particle = self.particles[i]
            particle.update(self.dt, self.gravity)

    cdef list check_collision(self):
        cdef int grid_size
        cdef dict grid
        cdef tuple key
        cdef list collision_pairs

        grid_size = 50
        grid = {}

        for i in range(self.n_particles):
            particle = self.particles[i]
            key = (
                particle.position[0] // grid_size,
                particle.position[1] // grid_size,
            )

            if key not in grid:
                grid[key] = []
            grid[key].append(particle)

        collision_pairs = []
        for cell_particles in grid.values():
            for i in range(len(cell_particles)):
                particle = cell_particles[i]
                for j in range(i + 1, len(cell_particles)):
                    other = cell_particles[j]
                    if particle.collides_with(other):
                        collision_pairs.append((particle, other))

        return collision_pairs

    cdef void resolve_collisions(self, list collision_pairs):
        cdef cnp.ndarray direction, normal, dv, impulse
        cdef double distance, dv_along_normal, magnitude

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

    cdef void enforce_constraints(self):
        cdef double X_MIN, Y_MIN, X_MAX, Y_MAX, x, y

        for i in range(self.n_particles):
            particle = self.particles[i]
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
