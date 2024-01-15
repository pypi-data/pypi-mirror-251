from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Graph package'
LONG_DESCRIPTION = """
 grphpkg is a simple graph library that has DFS and BFS
 implemented that you can create your own operation."""

# Setting up
setup(
    name="grphpkg",
    version=VERSION,
    author="Vu Diep",
    author_email="vudiep411@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="https://github.com/vudiep411/grphpkg",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "matplotlib"
    ],
    keywords=['python', 'data structure', 'graph', 'visualization'],
)

