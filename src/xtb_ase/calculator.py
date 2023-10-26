"""
ASE calculator for xtb_ase
"""
from __future__ import annotations

from pathlib import Path
from shutil import which
from subprocess import check_call
from typing import TYPE_CHECKING

from ase.calculators.genericfileio import CalculatorTemplate, GenericFileIOCalculator
from ase.units import Bohr, Hartree
from monty.json import jsanitize

from xtb_ase.io import read_xtb, write_xtb

if TYPE_CHECKING:
    from ase.atoms import Atoms

_LABEL = "xtb"


class xTBProfile:
    """
    xTB profile
    """

    def __init__(self, argv):
        self.argv = argv

    def run(self, directory, inputfile, outputfile):
        cmd = self.argv + [str(inputfile)]
        with open(outputfile, "w") as fd:
            check_call(cmd, stdout=fd, cwd=directory)


class xTBTemplate(CalculatorTemplate):
    """
    xTB template
    """

    def __init__(self):
        super().__init__(
            name=_LABEL, implemented_properties=["energy", "forces", "attributes"]
        )

        self.input_file = f"{_LABEL}.inp"
        self.output_file = f"{_LABEL}.out"

    def execute(self, directory, profile) -> None:
        profile.run(directory, self.input_file, self.output_file)

    def write_input(self, directory: Path, atoms: Atoms, parameters, properties):
        parameters = dict(parameters)

        kw = dict(
            charge=0,
            mult=1,
            orcasimpleinput="B3LYP def2-TZVP",
            orcablocks="%pal nprocs 1 end",
        )
        kw.update(parameters)

        write_xtb(directory / self.input_file, atoms, kw)

    def read_results(self, directory: Path):
        """
        Use cclib to read the results from the xTB calculation.
        """
        cclib_obj = read_xtb(directory / self.output_file)

        energy = cclib_obj.scfenergies[-1] * Hartree if cclib_obj.scfenergies else None
        forces = (
            cclib_obj.grads[-1, :, :] * (Hartree / Bohr) if cclib_obj.grads else None
        )

        return {
            "energy": energy,
            "forces": forces,
            "attributes": jsanitize(cclib_obj.getattributes()),
        }


class xTB(GenericFileIOCalculator):
    """
    xTB calculator
    """

    def __init__(
        self,
        *,
        profile: xTBProfile | None = None,
        directory: Path | str = ".",
        **kwargs,
    ):
        self.directory = Path(directory).expanduser()

        if not bool(which("xtb")):
            raise FileNotFoundError("xtb executable not found in PATH")

        super().__init__(
            template=xTBTemplate(),
            profile=xTBProfile(["xtb"]) or profile,
            directory=directory,
            parameters=kwargs,
        )
