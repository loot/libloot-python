libloot-python
==============

![CI](https://github.com/loot/libloot-python/workflows/CI/badge.svg?branch=master&event=push)
[![Documentation Status](https://readthedocs.org/projects/loot-api-python/badge/)](http://loot-api-python.readthedocs.io/)

A Python module that wraps libloot, generated by [pybind11](https://github.com/pybind/pybind11). Not everything in the API is exposed: coverage can be extended on request (or by pull request).

## Downloads

Snapshot builds are available on [Artifactory](https://loot.jfrog.io/ui/repos/tree/General/libloot-python). The snapshot build archives are named like so:

```
libloot-python-<short revision ID>-python<python version>-win<architecture>.zip
```

For example `libloot-python-94de368-python3.7-win32.zip` was built using the revision with shortened commit ID `94de368`.

## Documentation

The documentation can be found online at [Read The Docs](http://loot-api-python.readthedocs.org/).

## Build Instructions

The module's build system uses [CMake](https://cmake.org/) and requires [Python](https://www.python.org). Make sure they're installed, then run CMake, and build the generated solution file.

Only Windows support has been tested, though Linux builds should also be possible.
