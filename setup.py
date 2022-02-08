#!/usr/bin/env python

import setuptools
import pathlib

pwd = pathlib.Path(__file__).parent
description = (pwd / "README.md").read_text()

setuptools.setup(name="parler-api",
	version="2.0",
	description="Parler API library - v2",
	long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/konradit/parler-py-api",
	author="Konrad Iturbe",
	author_email="mail@chernowii.com",
	packages=setuptools.find_packages(),
	python_requires=">=3.6",
    install_requires=["requests", "marshmallow"],
)
