"""Init data"""
from __future__ import annotations

from importlib.metadata import version

from xtb_ase.calculator import XTB, XTBProfile

__all__ = ["XTB", "XTBProfile"]

__version__ = version("xtb_ase")
