# Basic Usage

## Overview

The `xtb_ase` package behaves very similarly to other ASE calculators. We demonstrate some basic examples here.

## Minimal Example

Let's start with a single-point energy calculation of water:

```python
from ase.build import molecule

from xtb_ase import XTB

atoms = molecule("H2O")
atoms.calc = XTB()

atoms.get_potential_energy()

print(atoms.calc.results)
```

!!! Info

    The output of the print statement is shown below:

    ```python
    {'energy': -137.9677709332199,
    'attributes': {'atomcharges': {'mulliken': [-0.561, 0.281, 0.281]},
    'atomcoords': [[]],
    'atomnos': [8, 1, 1],
    'charge': 0,
    'coreelectrons': [0, 0, 0],
    'grads': [[[2.6396675027566e-17, -1.5804343070521e-16, 0.014575739757803],
        [-3.1317598233266e-17, 0.0029851379960905, -0.0072878698789013],
        [4.9209232057001e-18, -0.0029851379960903, -0.0072878698789012]]],
    'homos': [0, 1, 2, 3],
    'metadata': {'package': 'xTB',
    'methods': ['GFN2-xTB'],
    'success': True,
    'package_version': '6.6.1',
    'keywords': ['xtb',
        '--chrg',
        '0',
        '--uhf',
        '0',
        '--gfn',
        '2',
        '--grad',
        '--input',
        'xtb.inp',
        'coord.xyz'],
    'coord_type': 'xyz',
    'wall_time': ['0:00:00.748000'],
    'cpu_time': ['0:00:12.070000']},
    'moenergies': [[-18.5113, -15.3777, -14.0152, -12.1663, 2.0111, 6.0623]],
    'mult': 1,
    'natom': 3,
    'scfenergies': [-137.9677709332199]},
    'forces': array([[ 1.35737159e-15, -8.12691990e-15,  7.49514668e-01],
            [-1.61041564e-15,  1.53501966e-01, -3.74757334e-01],
            [ 2.53044043e-16, -1.53501966e-01, -3.74757334e-01]])}
    ```

## The Calculator Results

First and foremost, the logfile will automatically be written out as `xtb.out`, which can be investigated as you see fit.

The `results` attribute of the calculator is a dictionary that contains all the parsed information from an `xtb` run. It contains the following keys:

- `energy`: The total energy of the system in units of eV. This can be accessed directly via `atoms.get_potential_energy()`.
- `forces`: The forces on the atoms in units of eV/Å. This can be accessed directly via `atoms.get_forces()`.
- `attributes`: A dictionary containing all the parsed [cclib attributes](https://cclib.github.io/data_dev.html). The units are those specified by cclib.

## A Relaxation

### Using ASE as the Optimizer

```python
from ase.build import molecule
from ase.optimize import BFGS

from xtb_ase import XTB

atoms = molecule("H2O")
atoms.calc = XTB()
dyn = BFGS(atoms)

dyn.run(fmax=0.01)

print(atoms.calc.results)
```

### Using xTB as the Optimizer

```python
from ase.build import molecule

from xtb_ase import XTB, XTBProfile

atoms = molecule("H2O")
profile = XTBProfile(["xtb", "--opt"])
atoms.calc = XTB(profile=profile)

atoms.get_potential_energy()

print(atoms.calc.results)
```

!!! Warning "On the Mutability of `Atoms`"

    In contrast with the use of an ASE optimizer, the input `Atoms` object is not updated in-place when calling `.get_potential_energy()`. Instead, this information is stored in `atoms.calc.results["final_atoms"]`.
