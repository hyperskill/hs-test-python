# hs-test-python

Python testing library for Hyperskill projects

It is a framework that simplifies testing educational projects for [Hyperskill](https://hyperskill.org).

The main features are:
* black box testing
* multiple types of tests in a simple unified way (without stdin, with stdin, files, Django, Flask, Matplotlib)
* generating learner-friendly feedback (filtering stack-traces, hints)

## Installation

Install the package directly from GitHub:

```bash
pip install https://github.com/hyperskill/hs-test-python/archive/release.tar.gz
```

The package includes pre-built wheels for psutil, so you don't need a C++ compiler to install it.

## Development

To contribute to the project:

1. Clone the repository
2. Install dependencies with poetry:
```bash
poetry install
```

To learn how to use this library you can go here:
https://github.com/hyperskill/hs-test-python/wiki
