#!/usr/bin/env python3

import setuptools

import saur.version as ver

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
        name='SAUR',
        version=ver.__version__,
        description='The Emporer of AUR scripts! Manage a local repository with easy.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Hans-Nikolai Viessmann',
        author_email='hans@viess.mn',
        url='https://github.com/hv15/saur',
        license='Unlicense',
        packages=setuptools.find_packages(exclude=('tests', 'docs')),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX",
            "Topic :: System :: Archiving :: Packaging",
            "Natural Language :: English",
            ],
        entry_points={
            'console_scripts' : [
                'saur = saur.console:run'
                ]
            },
        )
