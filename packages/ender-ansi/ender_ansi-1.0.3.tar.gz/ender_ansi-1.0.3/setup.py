from setuptools import setup, find_packages
import os

VERSION = '1.0.3'
DESCRIPTION = '🌈 uwu cutesy rainbow text <3 ✨'

# Setting up
setup(
    name="ender_ansi",
    version=VERSION,
    author="Endercat126",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'colour', 'ansi'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)