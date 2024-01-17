# Setup file for myIPstats package on PyPI.

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="myIPstats",
    version="1.4",
    author="Eric Dennis",
    author_email="ericdennis11@gmail.com",
    license="MIT",
    url="https://github.com/ericdennis7/myIPstats",
    
    description="A module to fetch your IP address information.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
