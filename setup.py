#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name='SAUR',
        version='1.0.0',
        description='The Emporer of AUR scripts! Manage a local repository with easy.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Hans-Nikolai Viessmann',
        author_email='hans@viess.mn',
        url='https://github.com/hv15/saur/',
        license='Unlicense',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Natural Language :: English",
            ],
        scripts=['saur.py']
        )
