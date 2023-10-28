# xtb_ase

Welcome to the documentation for [`xtb_ase`](https://github.com/Quantum-Accelerators/xtb_ase)!

## Motivation

The [`xtb` package](https://github.com/grimme-lab/xtb) is an excellent program that provides unified access to various extended tight-binding quantum chemistry methods.

There are several pre-existing Pythonic interfaces to the xTB suite of methods. The most notable include [`tblite`](https://github.com/tblite/tblite) and the now-deprecated [`xtb-python`](https://github.com/grimme-lab/xtb-python). However, these interfaces do not provide full access to all the functionality of `xtb`, making their utility somewhat limited.

The `xtb_ase` package aims to provide a fully featured [Atomic Simulation Environment (ASE)](https://gitlab.com/ase/ase) calculator for `xtb`. The `xtb_ase` package calls the `xtb` executable directly, uses [cclib](https://github.com/cclib/cclib) for the output parsing, and uses [Jinja](https://github.com/pallets/jinja) for the input file templating. This combination enables a lightweight and flexible interface to `xtb` that is fully compatible with the ASE framework.
