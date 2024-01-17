# Setup file for getmyip package on PiPy.

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name = "myIPstats",
    version = "1.0.0",
    author = "Eric Dennis",
    author_email = "ericdennis11@gmail.com",
    license = "MIT",
    url = "https://github.com/ericdennis7/myipaddress",
    
    description = "A module to fetch your IP address information.",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    package_dir = {"ip_address": "ip_address"},
    install_requires = [],

    packages = find_packages(),

    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
