import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "pysics.particle", ["pysics/particle.pyx"], include_dirs=[numpy.get_include()]
    ),
    Extension(
        "pysics.simulation",
        ["pysics/simulation.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()],
)
