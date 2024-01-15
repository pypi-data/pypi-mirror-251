# Data Utility Packages: _Core_

[![test](https://github.com/korawica/ddeutil/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/ddeutil/actions/workflows/tests.yml)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil)](https://pypi.org/project/ddeutil/)
[![size](https://img.shields.io/github/languages/code-size/korawica/ddeutil)](https://github.com/korawica/ddeutil)

**Table of Contents:**:

- [Features](#features)
  - [Base Utility Functions](#base-utility-functions)
  - [Utility Functions](#utility-functions)

The **Core Utility** package with the utility objects that was created with
sub-package namespace, `ddeutil`, for independent installation. This make this
package able to extend with any extension with this namespace. In the future,
this namespace able to scale out the coding with folder structure. You can add
any features that you want to install and import by `import ddeutil.{extension}`.

This package provide the Base Utility and Utility functions for any data package.

**Install from PyPI**:

```shell
pip install ddeutil
```

In the future, this namespace package will implement extension package for
dynamic installation such as you want to use file utility package that
implement by this namespace, you can install by `pip install ddeutil-file`.

## Features

### Base Utility Functions

```text
core.base
    - cache
    - checker
    - convert
    - elements
    - hash
    - merge
    - prepare
    - sorting
    - splitter
```

### Utility Functions

```text
core
    - decorator
    - dtutils
    - randomly
```

## License

This project was licensed under the terms of the [MIT license](LICENSE).
