#!/usr/bin/env python

import setuptools
import pathlib
version = open("Parler/version.py").read().split('"')[1]

pwd = pathlib.Path(__file__).parent
description = (pwd / "README.md").read_text()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="parler-api",
    version=version,
    description="Parler API library - v2.7",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/konradit/parler-py-api",
    author="Konrad Iturbe",
    author_email="mail@chernowii.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
)
