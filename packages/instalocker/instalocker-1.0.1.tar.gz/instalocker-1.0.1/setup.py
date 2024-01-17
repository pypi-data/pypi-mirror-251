from setuptools import setup, find_packages

setup(
    name='instalocker',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'valclient',
        'colorama',
        'pystyle',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'instalocker=instalocker.instalocker:main'
        ]
    },
    package_data={
        'instalocker': ['images/1.ico'],
    },
)
