#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="pyodim",
    version="0.4",
    description="An ODIM hdf5 file reader.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlouf/pyodim",
    author="Valentin Louf",
    author_email="valentin.louf@bom.gov.au",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="odim h5 file reader",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires= ["numpy", "dask", "xarray", "h5py", "pyproj"],
    project_urls={
        "Bug Reports": "https://github.com/vlouf/pyodim/issues",
        "Source": "https://github.com/vlouf/pyodim/",
    },
)
