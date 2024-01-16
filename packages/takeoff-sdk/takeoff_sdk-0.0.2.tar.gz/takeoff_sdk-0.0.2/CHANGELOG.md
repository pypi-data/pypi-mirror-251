# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

- /

## [0.0.2] - 2024-01-15


### Added

- add attribute `refill_threshold` into schema, which is `TAKEOFF_REFILL_THRESHOLD` Env var
- add function `cleanup()` for cleaning up the docker container
- improve error traceback message. now spining takeoff will catch error message inside the docker and print it outside. 

## [0.0.1] - 2024-01-11

- initial release
- add takeoff python sdk, publishing on [PyPI](https://pypi.org/project/takeoff-sdk/)

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
