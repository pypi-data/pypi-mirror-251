# poetry-external-dependencies

The package is a [poetry plugin](https://python-poetry.org/docs/master/plugins/), it extend the capability of poetry when installed in your environment.

When running `poetry build` this plugin will look in the project toml configuration for an `external` section and adds `dependencies` in the built package's metadata as a [`Requires-External` entry](https://packaging.python.org/en/latest/specifications/core-metadata/#requires-external-multiple-use).

#####Toml example:
```
[external]
dependencies = ["pkg:generic/libsomething"]
```

The toml syntax is not final, it is currently drafted in [PEP725](https://peps.python.org/pep-0725/).
Only `dependencies` are supported by this plugin, `host-requires` and `build-requires` are ignored, `optional-xxx` fields are also ignored.


## Installation

Poetry doesn't currently support auto installation of plugin from a pyproject.toml, in order to use this plugin you will need to install it using pip:


```bash
$ pip install poetry-external-dependencies
```
This needs to be installed in the same environnement as the one in which poetry is installed
