from ase.build import molecule

from xtb_ase.calculator import XTB


def test_molecule_static(tmpdir):
    tmpdir.chdir()

    atoms = molecule("H2")
    atoms.calc = XTB()
    atoms.get_potential_energy()
    assert isinstance(atoms.calc.results["energy"], float)
    assert isinstance(atoms.calc.results["attributes"], dict)
