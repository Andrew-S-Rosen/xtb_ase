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

    class Results(TypedDict, total=False):
        energy: float  # eV
        forces: NDArray  # Nx3, eV/Å
        attributes: dict[str, Any] | None  # https://cclib.github.io/data_dev.html


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
            The command line arguments to the xTB executable. Do not specify an
            input file, i.e. --input (-I), or the geometry file, as these will be
            automatically added.

        Returns
        -------
        None
        """
        default_argv = ["xtb"]
        self.argv = argv or default_argv

    def run(
        self,
        directory: Path | str,
        input_filename: str,
        geom_filename: str,
        output_filename: str,
    ) -> None:
        """
        Run the xTB calculation.

        Parameters
        ----------
        directory
            The directory where the calculation will be run.
        input_filename
            The name of the input file present in the directory.
        geom_filename
            The name of the coordinates file present in the directory.
        output_filename
            The name of the log file to write to in the directory.

        Returns
        -------
        None
        """
        cmd = self.argv + ["--input", input_filename, geom_filename]
        with open(output_filename, "w") as fd:
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
            name=label,
            implemented_properties=["energy", "forces", "attributes"],
        )

        self.input_file = f"{label}.inp"
        self.output_file = f"{label}.out"
        self.periodic = None
        self.geom_file = None

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
        profile: XTBProfile,  # skipcq: PYL-W0613
        directory: Path | str,
        atoms: Atoms,
        parameters: dict[str, Any],
        properties: Any,  # skipcq: PYL-W0613
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
        if self.periodic and "--tblite" not in profile.argv:
            profile.argv.append("--tblite")

        write_xtb(
            atoms,
            directory / self.input_file,
            directory / self.geom_file,
            parameters=parameters,
        )

    def read_results(self, directory: Path | str) -> Results:
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
        cclib_obj = read_xtb(Path(directory) / self.output_file)

        energy = cclib_obj.scfenergies[-1]

        results = {
            "energy": energy,
            "attributes": jsanitize(cclib_obj.getattributes()),
        }

        if getattr(cclib_obj, "grads", None):
            results["forces"] = cclib_obj.grads[-1, :, :]

        return results

    def load_profile(self, cfg, **kwargs):
        return XTBProfile.from_config(cfg, self.name, **kwargs)


class XTB(GenericFileIOCalculator):
    """
    xTB calculator
    """

    def __init__(
        self,
        profile: XTBProfile | None = None,
        directory: Path | str = ".",
        **kwargs,
    ) -> None:
        """
        Initialize the xTB calculator.

        Parameters
        ----------
        profile
            An instantiated [xtb_ase.calculator.XTBProfile][] object to use.
        directory
            The path to the directory to run the xTB calculation in.
        **kwargs
            The xTB parameters to be written out to a detailed input file, e.g.
            `gfn={"method": 1}`. See https://github.com/grimme-lab/xtb/blob/main/man/xcontrol.7.adoc.

        Returns
        -------
        None
        """

        profile = profile or XTBProfile()
        directory = Path(directory).expanduser().resolve()

        super().__init__(
            template=_XTBTemplate(),
            profile=profile,
            directory=directory,
            parameters=kwargs,
        )
