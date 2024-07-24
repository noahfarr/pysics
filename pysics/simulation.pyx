import numpy as np
cimport numpy as cnp
cnp.import_array()

from tqdm import tqdm

from pysics.particle cimport Particle

cdef class Simulation:

    cdef cnp.ndarray[object, ndim=1] particles
    cdef int n_particles
    cdef double gravity
    cdef double dt
    cdef renderer
    cdef double WALL_DAMP
    cdef double RESTITUTION
    cdef int MIN_X
    cdef int MAX_X
    cdef int MIN_Y
    cdef int MAX_Y
    cdef int MAX_VEL

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

        self.MIN_X = 0
        self.MIN_Y = 0

        cdef tuple size = self.renderer.size
        self.MAX_X = 1200
        self.MAX_Y = 800

        self.MAX_VEL = 50

    cdef cnp.ndarray generate_particles(self, int n_particles):
        cdef int i
        cdef cnp.ndarray[object, ndim=1] particles
        cdef cnp.ndarray[double, ndim=1] x_positions, y_positions, x_velocities, y_velocities

        particles = np.empty(n_particles, dtype=Particle)

        x_positions = np.random.uniform(0, 1200, self.n_particles)
        y_positions = np.random.uniform(0, 800, self.n_particles)

        x_velocities = np.random.uniform(0, 50, self.n_particles)
        y_velocities = np.random.uniform(0, 50, self.n_particles)

        for i in range(n_particles):
            particles[i] = Particle(
                1.0, 10.0,
                np.array([0.0, 0.0]),
                np.array([x_positions[i], y_positions[i]]),
                np.array([x_velocities[i], y_velocities[i]]),
                np.array([0.0, 0.0])
            )

        return particles

    def simulate(self, double total_timesteps, bint render):
        cdef list collision_pairs
        cdef cnp.ndarray[double, ndim=1] x_positions, y_positions, radii
        cdef Particle particle

        for timestep in tqdm(np.arange(0.0, total_timesteps, self.dt)):
            self.step()

            collision_pairs = self.check_collisions()
            self.resolve_collisions(collision_pairs)
            self.enforce_constraints()

            x_positions = np.zeros(self.n_particles)
            y_positions = np.zeros(self.n_particles)
            radii = np.zeros(self.n_particles)
            for i in range(self.n_particles):
                particle = self.particles[i]
                x_positions[i] = particle.position[0]
                y_positions[i] = particle.position[1]
                radii[i] = particle.radius
                # print(particle.position)


            if render:
                self.renderer.render(x_positions, y_positions, radii)

    cdef step(self):
        cdef Particle particle
        for i in range(self.n_particles):
            particle = self.particles[i]
            particle.update(self.dt, self.gravity)

    cdef list check_collisions(self):
        cdef list collision_pairs
        cdef Particle particle, other

        collision_pairs = []
        for i in range(self.n_particles):
            particle = self.particles[i]
            for j in range(i + 1, self.n_particles):
                other = self.particles[j]
                if self.check_collision(particle, other):
                    collision_pairs.append((particle, other))

        return collision_pairs

    cdef void resolve_collisions(self, list collision_pairs):
        cdef cnp.ndarray direction, normal, dv, impulse
        cdef double distance, dv_along_normal, magnitude
        cdef Particle particle, other

        for i in range(len(collision_pairs)):
            particle = collision_pairs[i][0]
            other = collision_pairs[i][0]
            direction = other.position - particle.position
            distance = self.get_distance(particle, other)

            if distance > 0:
                normal = direction / distance
            else:
                normal = direction

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
        cdef Particle particle

        for i in range(self.n_particles):
            particle = self.particles[i]
            X_MIN = 0
            Y_MIN = 0
            X_MAX = 1200
            Y_MAX = 800

            # position = particle.position
            x = particle.position[0]
            y = particle.position[1]
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


    cdef double get_distance(self, Particle particle, Particle other):
        cdef double distance
        distance = np.linalg.norm(other.position - particle.position)
        return distance

    cdef bint check_collision(self, Particle particle, Particle other):
        cdef double distance
        cdef bint is_collision
        distance = self.get_distance(particle, other)
        is_collision = distance <= (particle.radius + other.radius)
        return is_collision
