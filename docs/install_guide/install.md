# Installation Guide

## Installing xTB

First, you'll need to install the xTB package. The easiest way to do this is via Conda:

```bash
conda install -c conda-forge xtb
```

## Installing Dependencies

Currently, the `xtb_ase` package relies on actively developed branches of `ase` and `cclib`. To install these, you can use the following commands:

```bash
pip install https://gitlab.com/ase/ase/-/archive/master/ase-master.zip
pip install git+https://github.com/cclib/cclib.git@refs/pull/1296/head
```

## Installing `xtb_ase`

Following this, you can then install `xtb_ase` as usual:

```bash
pip install git+https://github.com/Quantum-Accelerators/xtb_ase.git
```
