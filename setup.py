# setup.py
import numpy
from setuptools import setup, Extension
from Cython.Build import cythonize

# List of Cython extensions
extensions = [
    Extension("particle", ["pysics/particle.pyx"], include_dirs=[numpy.get_include()]),
    Extension(
        "simulation", ["pysics/simulation.pyx"], include_dirs=[numpy.get_include()]
    ),
]

setup(ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}))
