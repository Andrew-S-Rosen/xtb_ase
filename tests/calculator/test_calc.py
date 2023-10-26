from xtb_ase.calculator import XTB
from ase.build import bulk, molecule


def test_molecule_static(tmpdir):
    tmpdir.chdir()

    atoms = molecule("H2")
    atoms.calc = XTB()
    atoms.get_potential_energy()
    assert isinstance(atoms.calc.results["energy"], float)
    assert atoms.calc.results["forces"].shape == (2, 3)
    assert isinstance(atoms.calc.results["attributes"], dict)


def test_solid_static(tmpdir):
    tmpdir.chdir()

    atoms = bulk("Cu")
    atoms.calc = XTB()
    atoms.get_potential_energy()
    assert isinstance(atoms.calc.results["energy"], float)
    assert atoms.calc.results["forces"].shape == (1, 3)
    assert isinstance(atoms.calc.results["attributes"], dict)
