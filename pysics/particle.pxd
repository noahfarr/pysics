# particle.pxd
cimport numpy as cnp

cdef class Particle:
    cdef double mass
    cdef double radius
    cdef cnp.ndarray force
    cdef cnp.ndarray position
    cdef cnp.ndarray velocity
    cdef cnp.ndarray acceleration

    cdef void update(self, double dt, double gravity)
