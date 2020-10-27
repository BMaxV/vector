import os
import setuptools

setuptools.setup(
    name = "vector",
    version = "0.13",
    author = "Brumo Maximilian Voss",
    author_email = "bruno.m.voss@gmail.com",
    description = ("perform common 3d vector operations"),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    license = "MIT",
)
