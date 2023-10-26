"""
I/O for xTB
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ase.io import write
from cclib.io import ccread
from jinja2 import Template

if TYPE_CHECKING:
    from typing import Any

    from ase.atoms import Atoms
    from cclib.parser.data import ccData


def write_xtb(
    atoms: Atoms,
    directory: Path | str,
    input_file: Path | str,
    parameters: dict[str, Any],
) -> None:
    """
    Write out the input files for xTB.
    """

    template_str = """
    {% for key, value in parameters.items() %}
    ${{ key }}
    {% for inner_key, inner_value in value.items() %}
    {{ inner_key }}: {{ inner_value }}
    {% endfor %}
    $end

    {% endfor %}
    """
    directory = Path(directory)

    # Write the input file using the Jinja2 template
    input_text = Template(template_str).render(parameters=parameters)
    with open(directory / input_file, "w") as fd:
        fd.write(input_text)

    # Write the geometry file
    geom_file = "POSCAR" if atoms.pbc.any() else "coord.xyz"
    write(directory / geom_file, atoms)


def read_xtb(outputfile: Path | str) -> ccData:
    """
    Read the output files from xTB.
    """
    cclib_obj = ccread(outputfile)

    if not cclib_obj:
        msg = f"Could not read {outputfile}"
        raise RuntimeError(msg)

    return cclib_obj
