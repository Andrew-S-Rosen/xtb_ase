"""Init data"""
from __future__ import annotations

from importlib.metadata import version

from xtb_ase.calculator import XTB

__all__ = ["XTB"]

__version__ = version("xtb_ase")
