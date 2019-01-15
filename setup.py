import os
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "vector",
    version = "0.12",
    author = "Brumo Maximilian Voss",
    author_email = "bruno.m.voss@gmail.com",
    description = ("perform common 3d vector operations"),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    license = "MIT",
    #keywords = "sympy 3d",
   

    #install_requires=[
    #    'sympy',
    #]
    #long_description=read('README'),
 #   classifiers=[
 #       "Development Status :: 3 - Alpha",
 #       "Topic :: Utilities",
 #       "License :: OSI Approved :: BSD License",
 #   ],
)
