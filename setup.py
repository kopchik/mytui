#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name="mytui",
    version="1.0",
    author="Alexandre Kandalintsev",
    description="Text User Interface library",
    url="https://github.com/kopchik/mytui",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Beerware",
        "Operating System :: OS Independent",
    ),
    install_requires=['blessings'],
)
