# confidence_calculator/setup.py

from setuptools import setup, find_packages

setup(
    name='confidence_calculator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
    ],
)
