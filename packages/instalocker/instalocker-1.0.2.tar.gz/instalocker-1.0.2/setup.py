# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='instalocker',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'valclient',
        'colorama',
        'pystyle',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'instalocker = instalocker.instalocker:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)