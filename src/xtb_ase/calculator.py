"""
ASE calculator for xtb_ase
"""
from __future__ import annotations

from pathlib import Path
from subprocess import check_call
from typing import TYPE_CHECKING

from ase.calculators.genericfileio import CalculatorTemplate, GenericFileIOCalculator
from ase.units import Bohr, Hartree
from monty.json import jsanitize

from xtb_ase.io import read_xtb, write_xtb

if TYPE_CHECKING:
    from typing import Any, TypedDict

    from ase.atoms import Atoms
    from numpy.typing import NDArray

    class Results(TypedDict):
        energy: float  # eV
        forces: NDArray  # Nx3, eV/Å
        attributes: dict[str, Any] | None  # https://cclib.github.io/data.html

class XTBProfile:
    """
    xTB profile
    """

    def __init__(self, argv: list[str] | None = None) -> None:
        self.argv = argv or ["xtb"]

    def run(
        self,
        directory: Path | str,
        input_file: Path | str,
        geom_file: Path | str,
        output_file: Path | str,
    ) -> None:
        cmd = self.argv + ["--input", str(input_file), str(geom_file)]
        with open(output_file, "w") as fd:
            check_call(cmd, stdout=fd, cwd=directory)


class XTBTemplate(CalculatorTemplate):
    """
    xTB template
    """

    def __init__(self) -> None:
        label = "xtb"
        super().__init__(
            name=label, implemented_properties=["energy", "forces", "attributes"]
        )

        self.input_file = f"{label}.inp"
        self.output_file = f"{label}.out"

    def execute(self, directory, profile) -> None:
        """
        Run the xTB executable.
        """
        profile.run(directory, self.input_file, self.geom_file, self.output_file)

    def write_input(
        self, directory: Path | str, atoms: Atoms, parameters: dict[str, Any], properties: Any
    ) -> None:
        """
        Write the xTB input files.
        """
        self.periodic = True if atoms.pbc.all() else False
        self.geom_file = "POSCAR" if self.periodic else "coord.xyz"
        write_xtb(atoms, directory, self.input_file, parameters=parameters)

    def read_results(self, directory: Path) -> Results:
        """
        Use cclib to read the results from the xTB calculation.
        """
        cclib_obj = read_xtb(directory / self.output_file)

        energy = cclib_obj.scfenergies[-1] * Hartree
        forces = cclib_obj.grads[-1, :, :] * (Hartree / Bohr)

        return {
            "energy": energy,
            "forces": forces,
            "attributes": jsanitize(cclib_obj.getattributes()),
        }


class XTB(GenericFileIOCalculator):
    """
    xTB calculator
    """

    def __init__(
        self,
        profile: XTBProfile | None = None,
        directory: Path | str = ".",
        **parameters,
    ) -> None:
        profile = XTBProfile() or profile
        directory = Path(directory).expanduser().resolve()

        super().__init__(
            template=XTBTemplate(),
            profile=profile,
            directory=directory,
            parameters=parameters,
        )
