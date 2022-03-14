#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), "r") as file:
    install_requires = [
        line.strip() for line in file.readlines() if bool(line.strip()) and not line.strip().startswith("#")
    ]

setup(
    name="flavours",
    version="0.0.1",
    description="Pythonic Font Editor",
    license="apache-2.0",
    author="Yanone",
    author_email="flavours@yanone.de",
    url="https://github.com/flavoursapp/flavours",
    install_requires=install_requires,
    # package_dir={"": "Lib"},
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["flavours = flavours.cli:main"]},
)
