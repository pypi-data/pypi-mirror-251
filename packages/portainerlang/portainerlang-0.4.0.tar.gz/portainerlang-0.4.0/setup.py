# setup.py
from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return [line.strip() for line in req 
                if line.strip() and not line.startswith('#') and not line.startswith('-i')]

setup(
    name='portainerlang',
    version='0.4.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'portainerlang=portainerlang.main:main',
        ],
    },
)
