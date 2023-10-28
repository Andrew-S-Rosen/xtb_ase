# Setting xTB Parameters

## Simple Input

The `xtb_ase` calculator lets you set any of the typical [command-line arguments](https://xtb-docs.readthedocs.io/en/latest/commandline.html) for `xtb`.

The `xtb_ase` calculator uses a "profile" system to set how the `xtb` executable is called. By default, the `xtb_ase` calculator will run via `xtb --parallel <NCPUS>` where `<NCPUS>` is the number of accessible CPUs.

If you want to change the default command-line arguments, you can do so by instantiating a new profile. For example, to run the `xtb` executable as `xtb --gfn 1`:

```python
from ase.build import molecule
from xtb_ase import XTB, XTBProfile

atoms = molecule("H2O")

profile = XTBProfile(["xtb", "--gfn", "1"])
atoms.calc = XTB(profile=profile)

atoms.get_potential_energy()
print(atoms.calc.results)
```

!!! Info

    ```python
    {'attributes': {'charge': 0,
                    'homos': [0, 1, 2, 3],
                    'metadata': {'coord_type': 'xyz',
                                'cpu_time': ['0:00:00.065000'],
                                'methods': ['GFN1-xTB'],
                                'package': 'xTB',
                                'package_version': '6.6.1',
                                'success': True,
                                'wall_time': ['0:00:00.005000']},
                    'moenergies': [[-20.615,
                                    -16.5944,
                                    -14.9473,
                                    -13.6057,
                                    -4.3471,
                                    -1.4108,
                                    8.5045,
                                    12.0027]],
                    'scfenergies': [-156.96750016825985]},
    'energy': -156.96750016825985}
    ```

The logfile will automatically be written out as `xtb.out`, which can also be investigated as you see fit.

!!! Note

    You should never specify the `--input` (`-I`) or coordinate file command-line arguments. The `xtb_ase` calculator will take care of those automatically.

## Detailed Input

For more complex inputs, xTB supports a [detailed input](https://xtb-docs.readthedocs.io/en/latest/xcontrol.html) format called [`xcontrol`](https://github.com/grimme-lab/xtb/blob/main/man/xcontrol.7.adoc). This is also supported by the `xtb_ase` calculator, but instead of passing the arguments as an adjustment to the executable call in the `XTBProfile`, we modify the parameters of the `XTB` calculator instance.

The same example as above can be run via the detailed input as follows:

```python
from ase.build import molecule
from xtb_ase import XTB

atoms = molecule("H2O")

atoms.calc = XTB(gfn={"method": 1})

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
