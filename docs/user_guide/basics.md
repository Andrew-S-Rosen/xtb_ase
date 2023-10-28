# Basic Usage

## Overview

The `xtb_ase` package behaves very similarly to other ASE calculators. Unlike most calculators, however, we have taken the liberty to store as many properties as possible in the `.results` attribute of the calculator. We demonstrate some basic examples below.

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

    The output of the pretty print statement is shown below:

    ```python
    {'attributes': {'atomcharges': {'mulliken': [-0.561, 0.281, 0.281]},
                    'charge': 0,
                    'homos': [0, 1, 2, 3],
                    'metadata': {'coord_type': 'xyz',
                                'cpu_time': ['0:00:00.119000'],
                                'methods': ['GFN2-xTB'],
                                'package': 'xTB',
                                'package_version': '6.6.1',
                                'success': True,
                                'wall_time': ['0:00:00.012000']},
                    'moenergies': [[-18.5113,
                                    -15.3777,
                                    -14.0152,
                                    -12.1663,
                                    2.0111,
                                    6.0623]],
                    'scfenergies': [-137.9677709332199]},
    'energy': -137.9677709332199}
    ```

## The Calculator Results

The `results` attribute of the calculator is a dictionary that contains all the parsed information from an `xtb` run. It contains the following keys:

- `energy`: The total energy of the system in units of eV. This can be accessed directly via `atoms.get_potential_energy()`.
- `forces`: The forces on the atoms in units of eV/Å. This can be accessed directly via `atoms.get_forces()`.
- `attributes`: A dictionary containing all the parsed [cclib attributes](https://cclib.github.io/data_dev.html). The units are those specified by cclib.

Regarding the `Atoms` object following a calculation, we have made the decision to ensure that its atomic configuration (e.g. positions) reflect the final geometry rather than the input geometry. This is not the case for all ASE calculators, but we believe it is the most intuitive behavior.
