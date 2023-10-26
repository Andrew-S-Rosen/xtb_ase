from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from cclib.io import ccread

if TYPE_CHECKING:
    from typing import Any

    from ase.atoms import Atoms


def write_xtb(inputfile: Path, atoms: Atoms, kw: dict[str, Any]):
    return


def read_xtb(outputfile: Path):
    cclib_obj = ccread(outputfile)

    if not cclib_obj:
        msg = f"Could not read {outputfile}"
        raise RuntimeError(msg)

    return cclib_obj
