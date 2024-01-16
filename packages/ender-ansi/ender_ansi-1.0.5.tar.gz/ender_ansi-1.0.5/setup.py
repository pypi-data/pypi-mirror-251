from setuptools import setup, find_packages
import os

VERSION = '1.0.5'
DESCRIPTION = '🌈 uwu cutesy rainbow text <3 ✨'

pypi_url = 'https://pypi.org/project/ender-ansi/'
github_url = 'https://github.com/endercat126/ender-ansi/'

# Setting up
setup(
    name="ender_ansi",
    version=VERSION,
    author="Endercat126",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8').read(),
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'colour', 'ansi'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    url=github_url,
    project_urls={
        "Source": github_url
    }
)