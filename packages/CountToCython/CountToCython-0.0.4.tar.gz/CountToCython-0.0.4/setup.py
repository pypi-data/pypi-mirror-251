from setuptools import setup, find_packages
from Cython.Build import cythonize
import os

setup(
    name = "CountToCython",
    description="Module containing fast counting methods by using Cython.",
    long_description="Module containing fast counting methods by using Cython.",
    version="0.0.4",
    keywords = [
        "counting",
        "cython",
        "Fast",
        "Beginner Friendly",
        "Python",
        "Cython",
        "Hybrid",
    ],
    #ext_modules = cythonize([
        #f".\\CountTo\\CountMainFuncs.pyx",
    #],
    #annotate=True
    #),
    packages=find_packages(),
    install_requires=[
        "Cython",
        "importlib",
    ],
)