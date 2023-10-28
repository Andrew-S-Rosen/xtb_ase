# Contributing

## General

We certainly welcome bugfixes and contributions as pull requests (PRs). All PRs must come with associated unit tests and pass the test suite in order to be merged.

## Depenendencies

To install the dependencies for the test suite, install the `[dev]` extras:

```bash
pip install -e .[dev]
```

To install the dependencies for the documentation, install the `[docs]` extras:

```bash
pip install -e .[docs]
```

## Running the Tests

To run the test suite, use the following command in the base directory or `tests` directory:

```bash
pytest .
```

## Formatting

All code for `xtb_ase` is formatted using `black`, `isort`, and `ruff` (although this will be fixed automatically after your PR is merged).

## Building the Docs

To build the documentation, run the following in the base directory:

```bash
mkdocs serve
```
