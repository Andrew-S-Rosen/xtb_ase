# Setting xTB Parameters

## Simple Input

The `xtb_ase` calculator lets you set any of the typical [command-line arguments](https://xtb-docs.readthedocs.io/en/latest/commandline.html) for `xtb`.

The `xtb_ase` calculator uses a "profile" system to set how the `xtb` executable is called. By default, the `xtb_ase` calculator will run via `xtb --parallel <NCPUS>` where `<NCPUS>` is the number of accessible CPUs.

If you want to change the default command-line arguments, you can do so by instantiating a new profile. For example, to run the `xtb` executable as `xtb --opt --gfn 1`:

```python
from ase.build import molecule
from xtb_ase import XTB, XTBProfile

atoms = molecule("H2O")

profile = XTBProfile(["xtb", "--opt", "--gfn", "1"])
atoms.calc = XTB(profile=profile)

atoms.get_potential_energy()
print(atoms.calc.results)
```

!!! Info

    ```python
    {'attributes': {'atomcoords': [[0.0, 1.16e-11, 0.10114745079573],
                                   [0.0, 0.77088618141561, -0.46798972539333],
                                   [0.0, -0.77088618142721, -0.4679897254024]],
                    'atomnos': [8, 1, 1],
                    'charge': 0,
                    'coreelectrons': [0, 0, 0],
                    'homos': [0, 1, 2, 3],
                    'metadata': {'coord_type': 'xyz',
                                 'cpu_time': ['0:00:00.197000'],
                                 'methods': ['GFN1-xTB'],
                                 'package': 'xTB',
                                 'package_version': '6.6.1',
                                 'success': True,
                                 'wall_time': ['0:00:00.016000']},
                    'moenergies': [[-20.6262,
                                    -16.6667,
                                    -14.8617,
                                    -13.6046,
                                    -4.2577,
                                    -1.3582,
                                    9.4794,
                                    12.3964]],
                    'natom': 3,
                    'scfenergies': [-156.97635541503533]},
     'energy': -156.97635541503533}
    ```

!!! Note

    You should never specify the `--input` (`-I`) or coordinate file command-line arguments. The `xtb_ase` calculator will take care of those automatically.

## Detailed Input

For more complex inputs, xTB supports a [detailed input](https://xtb-docs.readthedocs.io/en/latest/xcontrol.html) format called [`xcontrol`](https://github.com/grimme-lab/xtb/blob/main/man/xcontrol.7.adoc). This is also supported by the `xtb_ase` calculator, but instead of passing the arguments as an adjustment to the executable call in the `XTBProfile`, we modify the parameters of the `XTB` calculator instance. If desired, both an `XTBProfile` and `XTB` parameters can be supplied.

```python
from ase.build import molecule
from xtb_ase import XTB, XTBProfile

atoms = molecule("H2O")

profile = XTBProfile(["xtb", "--opt"])
atoms.calc = XTB(profile=profile, gfn={"method": 1})

atoms.get_potential_energy()
print(atoms.calc.results)
```

An `xcontrol` file will be automatically written out to the runtime directory as `xtb.inp`.

!!! Warning

    The `xtb` code automatically ignores invalid parameters in the `xcontrol` file. When setting up a new calculation, it is recommended to check the `xtb.inp` and `xtb.out` files to ensure that the parameters were set correctly.

## Memory and Parallelization

The typical `xtb` suggestions apply when dealing with memory and parallelization, and `xtb_ase` lets the user make these decisions for themselves.

For instance, most users will benefit from [unlimiting the system stack](https://xtb-docs.readthedocs.io/en/latest/setup.html#setting-up-xtb):

```bash
ulimit -s unlimited
```

Additionally, one can speed up calculations by specifiying the `OMP_NUM_THREADS`, `OMP_MAX_ACTIVE_LEVELS`, and/or `MKL_NUM_THREADS` environment variables as described in the [xTB manual](https://xtb-docs.readthedocs.io/en/latest/setup.html#parallelisation).
