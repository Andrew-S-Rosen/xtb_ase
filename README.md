# xtb_ase

![tests](https://github.com/quantum-accelerators/xtb_ase/actions/workflows/tests.yaml/badge.svg)

A fully featured ASE calculator for the [xTB code](https://xtb-docs.readthedocs.io/en/latest/). It is maintained by the [Rosen Research Group](https://rosen.cbe.princeton.edu/) at Princeton University.

## Documentation

<p align="center">
  📖 <a href="https://andrew-s-rosen.github.io/xtb_ase/"><b><i>Read the Documentation!</i></b></a> 📖
</p>

## Motivation

The [`xtb` package](https://github.com/grimme-lab/xtb) is an excellent program that provides unified access to various extended tight-binding quantum chemistry methods.

There are several pre-existing Pythonic interfaces to the xTB suite of methods. The most notable include [`tblite`](https://github.com/tblite/tblite) and the now-deprecated [`xtb-python`](https://github.com/grimme-lab/xtb-python). However, these interfaces do not provide full access to all the functionality of `xtb`, making their utility somewhat limited.

The `xtb_ase` package aims to provide a fully featured [Atomic Simulation Environment (ASE)](https://gitlab.com/ase/ase) calculator for `xtb`. The `xtb_ase` package calls the `xtb` executable directly, uses [cclib](https://github.com/cclib/cclib) for the output parsing, and uses [Jinja](https://github.com/pallets/jinja) for the input file templating. This combination enables a lightweight and flexible interface to `xtb` that is fully compatible with the ASE framework.

## License

`xtb_ase` is released under a [BSD 3-Clause license](https://github.com/quantum-accelerators/xtb_ase/blob/main/LICENSE.md).
