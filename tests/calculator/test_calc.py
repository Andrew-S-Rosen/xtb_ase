from xtb_ase.calculator import xTB
from ase.build import bulk, molecule

def test_molecule():
    atoms = molecule("H2")
    atoms.calc = xTB()
    atoms.get_potential_energy()
    assert isinstance(atoms.calc.results["energy"], float)
    assert atoms.calc.results["forces"].shape == (2, 3)
    assert isinstance(atoms.calc.results["attributes"], dict)

def test_solid():
    atoms = bulk("Cu")
    atoms.calc = xTB()
    atoms.get_potential_energy()
    assert isinstance(atoms.calc.results["energy"], float)
    assert atoms.calc.results["forces"].shape == (1, 3)
    assert isinstance(atoms.calc.results["attributes"], dict)
