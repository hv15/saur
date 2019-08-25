# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- include a setuptools `setup.py` script for potential distribution
- git ignore for python projects
- documentation to `sample_config.ini` file

## Changed
- use subparser of `argparse` - makes subcommand handling cleaner

## [1.0.0] - 2017-06-20
### Added
- we now have an offical version
- princple feature are implemented
  - we can fetch aur packages and patch various files
  - we can sync and build the fetched aur packages
  - packages are appended to the local repository
- support GPG signing of packages and repository

[Unreleased]: https://github.com/hv15/saur/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/hv15/saur/releases/v1.0.0

