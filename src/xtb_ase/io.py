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
    input_filepath: Path | str,
    geom_filepath: Path | str,
    parameters: dict[str, Any],
) -> None:
    """
    Write out the input files for xTB.

    Parameters
    ----------
    atoms
        The ASE atoms object.
    input_filepath
        The path to the xTB input file.
    geom_filepath
        The path to the xTB geometry file.
    parameters
        The xTB parameters to use, formatted as a dictionary.

    Returns
    -------
    None
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

    # Write the input file using the Jinja2 template
    input_text = Template(template_str).render(parameters=parameters)
    with open(input_filepath, "w") as fd:
        fd.write(input_text)

    # Write the geometry file
    write(geom_filepath, atoms)


def read_xtb(output_filepath: Path | str) -> ccData:
    """
    Read the output files from xTB.

    Parameters
    ----------
    output_filepath
        The path to the xTB output file.
    
    Returns
    -------
    cclib_obj
        The cclib object containing the xTB results.
    """
    cclib_obj = ccread(output_filepath)

    if not cclib_obj:
        msg = f"Could not read {output_filepath}"
        raise RuntimeError(msg)

    return cclib_obj
