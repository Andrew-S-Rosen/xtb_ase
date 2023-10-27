"""
ASE calculator for xtb_ase
"""
from __future__ import annotations

from pathlib import Path
from subprocess import check_call
from typing import TYPE_CHECKING

from ase.calculators.genericfileio import CalculatorTemplate, GenericFileIOCalculator
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
        """
        Initialize the xTB profile.

        Parameters
        ----------
        argv
            The command line arguments to the xTB executable.

        Returns
        -------
        None
        """
        self.argv = argv or ["xtb"]

    def run(
        self,
        directory: Path | str,
        input_file: str,
        geom_file: str,
        output_file: str,
    ) -> None:
        cmd = self.argv + ["--input", str(input_file), str(geom_file)]
        with open(output_file, "w") as fd:
            check_call(cmd, stdout=fd, cwd=directory)


class _XTBTemplate(CalculatorTemplate):
    """
    xTB template
    """

    def __init__(self) -> None:
        """
        Initialize the xTB template.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        label = "xtb"
        super().__init__(
            name=label, implemented_properties=["energy", "forces", "attributes"]
        )

        self.input_file = f"{label}.inp"
        self.output_file = f"{label}.out"

    def execute(self, directory: Path | str, profile: XTBProfile) -> None:
        """
        Run the xTB executable.

        Parameters
        ----------
        directory
            The path to the directory to run the xTB executable in.
        profile
            The xTB profile to use.

        Returns
        -------
        None
        """
        profile.run(directory, self.input_file, self.geom_file, self.output_file)

    def write_input(
        self,
        directory: Path | str,
        atoms: Atoms,
        parameters: dict[str, Any],
        properties: Any,
    ) -> None:
        """
        Write the xTB input files.

        Parameters
        ----------
        directory
            The path to the directory to write the xTB input files in.
        atoms
            The ASE atoms object to write.
        parameters
            The xTB parameters to use, formatted as a dictionary.
        properties
            This is needed the base class and should not be explicitly specified.

        Returns
        -------
        None
        """
        self.periodic = bool(atoms.pbc.all())
        self.geom_file = "POSCAR" if self.periodic else "coord.xyz"
        write_xtb(
            atoms,
            directory / self.input_file,
            directory / self.geom_file,
            parameters=parameters,
        )

    def read_results(self, directory: Path) -> Results:
        """
        Use cclib to read the results from the xTB calculation.

        Parameters
        ----------
        directory
            The path to the directory to read the xTB results from.

        Returns
        -------
        Results
            The xTB results, formatted as a dictionary.
        """
        cclib_obj = read_xtb(directory / self.output_file)

        energy = cclib_obj.scfenergies[-1]
        forces = cclib_obj.grads[-1, :, :]

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
        """
        Initialize the xTB calculator.

        Parameters
        ----------
        profile
            The xTB profile to use.
        directory
            The path to the directory to run the xTB executable in.
        parameters
            The xTB parameters to use.
        """

        profile = profile or XTBProfile()
        directory = Path(directory).expanduser().resolve()

        super().__init__(
            template=_XTBTemplate(),
            profile=profile,
            directory=directory,
            parameters=parameters,
        )
