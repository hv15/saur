# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 04.12.2021
### Added
- include a setuptools `setup.py` script for potential distribution
- testsuite for aur package (WIP)

## Changed
- refactor code
- no long use `aur-sync`, instead use fetch/build manually

## [1.1.0] - 04.11.2019
### Added
- git ignore for python projects
- add exclude flag to `sync` command, allowing packages to be skipped over
- documentation to `sample_config.ini` file
- support rebuild of packages (must be specifed on command line)

## Changed
- use subparser of `argparse` - makes subcommand handling cleaner
- improve list print out
- improve error message on command

## [1.0.0] - some unknown date from the mists of time
### Added
- we now have an offical version
- princple feature are implemented
  - we can fetch aur packages and patch various files
  - we can sync and build the fetched aur packages
  - packages are appended to the local repository
- support GPG signing of packages and repository

[Unreleased]: https://github.com/hv15/saur/compare/v1.0.0...HEAD
[1.2.0]: https://github.com/hv15/saur/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/hv15/saur/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/hv15/saur/releases/v1.0.0
