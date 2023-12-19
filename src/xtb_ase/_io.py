"""
I/O for xTB
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from ase.io import read, write
from ase.units import Bohr, Hartree
from cclib.io import ccread
from jinja2 import Template
from monty.json import jsanitize

if TYPE_CHECKING:
    from typing import Any

    from ase.atoms import Atoms

    from xtb_ase.calculator import Results


def write_xtb_inputs(
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

    template_str = r"""
{% for key, value in parameters.items() %}
${{ key }}
{% for inner_key, inner_value in value.items() %}
    {% if inner_value is iterable and inner_value is not string %}
    {{ inner_key }}: {{ inner_value }}
    {% else %}
    {{ inner_key }}={{ inner_value }}
    {% endif %}
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


def read_xtb_results(
    output_file: Path | str,
    grad_file: Path | str | None,
    xtb_opt_file: Path | str | None,
) -> Results:
    """
    Read the output files from xTB.

    Parameters
    ----------
    output_file
        The path to the xTB output file.
    grad_file
        The path to the xTB gradient file.
    xtb_opt_file
        The path to the xTB .opt file.

    Returns
    -------
    Results
        The calculator results.
    """

    filepaths = [output_file]
    if grad_file.exists():
        filepaths.append(grad_file)

    cclib_obj = ccread(filepaths, logging.ERROR)
    energy = cclib_obj.scfenergies[-1]

    results = {
        "energy": energy,
        "attributes": jsanitize(cclib_obj.getattributes()),
    }
    if hasattr(cclib_obj, "grads"):
        forces = -cclib_obj.grads[-1, :, :] * Hartree / Bohr
        results["forces"] = forces

    xtb_opt_file = Path(xtb_opt_file)
    if xtb_opt_file.is_file():
        final_atoms = read(xtb_opt_file)
        results["final_atoms"] = final_atoms

    if forces is not None:
        results["forces"] = forces

    return dict(sorted(results.items()))
