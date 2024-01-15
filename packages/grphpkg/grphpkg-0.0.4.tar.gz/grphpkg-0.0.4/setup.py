from setuptools import setup, find_packages
import codecs
import os
import sys

VERSION = '0.0.4'
DESCRIPTION = 'Graph package'

with open("README.md", "r") as f:
    readme = f.read()

# Setting up
setup(
    name="grphpkg",
    version=VERSION,
    author="Vu Diep",
    author_email="vudiep411@gmail.com",
    description=DESCRIPTION,
    long_description=readme,
    url="https://github.com/vudiep411/grphpkg",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "matplotlib"
    ],
    keywords=['python', 'data structure', 'graph', 'visualization'],
)

