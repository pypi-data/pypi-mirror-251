#!/usr/bin/env python3

from setuptools import setup, find_packages

# Read file contents README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u1",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[],
    author="Mauricio Ortega",
    description="Test, hack4u course query library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
