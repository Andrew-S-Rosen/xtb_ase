import pytest
from ase.build import bulk, molecule
from numpy.testing import assert_allclose

from xtb_ase.calculator import XTB, XTBProfile


def test_molecule_static(tmpdir):
    tmpdir.chdir()

    atoms = molecule("H2O")
    atoms.calc = XTB()
    atoms.get_potential_energy()
    results = atoms.calc.results
    attributes = results["attributes"]
    assert results["energy"] == pytest.approx(-137.9677709332199)
    assert attributes["charge"] == 0
    assert attributes["metadata"]["package"] == "xTB"
    assert attributes["metadata"]["methods"] == ["GFN2-xTB"]
    assert attributes["metadata"]["coord_type"] == "xyz"
    assert attributes["scfenergies"] == results["energy"]
    assert "--gfn" not in attributes["metadata"]["keywords"]
    assert "--tblite" not in attributes["metadata"]["keywords"]
    assert "--parallel" not in attributes["metadata"]["keywords"]


def test_molecule_static_profile(tmpdir):
    tmpdir.chdir()

    atoms = molecule("H2O")
    atoms.calc = XTB(profile=XTBProfile(argv=["xtb", "--gfn", "1"]))
    atoms.get_potential_energy()
    results = atoms.calc.results
    attributes = results["attributes"]
    assert results["energy"] == pytest.approx(-156.96750016825985)
    assert attributes["charge"] == 0
    assert attributes["metadata"]["package"] == "xTB"
    assert attributes["metadata"]["methods"] == ["GFN1-xTB"]
    assert attributes["metadata"]["coord_type"] == "xyz"
    assert attributes["scfenergies"] == results["energy"]
    assert_allclose(attributes["atomcharges"]["cm5"], [-0.99277, 0.49638, 0.49638])
    assert_allclose(attributes["atomcharges"]["mulliken"], [-0.66558, 0.33279, 0.33279])
    assert "--gfn" in attributes["metadata"]["keywords"]
    assert "--tblite" not in attributes["metadata"]["keywords"]

def test_bulk_static(tmpdir):
    tmpdir.chdir()

    atoms = bulk("Cu")
    atoms.calc = XTB()
    atoms.get_potential_energy()
    results = atoms.calc.results
    attributes = results["attributes"]
    assert results["energy"] == pytest.approx(-318.8584638)
    assert attributes["metadata"]["package"] == "xTB"
    assert attributes["metadata"]["coord_type"] == "POSCAR"
    assert attributes["scfenergies"] == results["energy"]
    assert "--tblite" in attributes["metadata"]["keywords"]

def test_bulk_static_gfn1(tmpdir):
    tmpdir.chdir()

    atoms = bulk("Cu")
    atoms.calc = XTB(profile=XTBProfile(argv=["xtb", "--gfn", "1"]))
    atoms.get_potential_energy()
    results = atoms.calc.results
    attributes = results["attributes"]
    assert results["energy"] == pytest.approx(-130.73083354749846)
    assert attributes["metadata"]["package"] == "xTB"
    assert attributes["metadata"]["coord_type"] == "POSCAR"
    assert attributes["scfenergies"] == results["energy"]
    assert "--gfn" in attributes["metadata"]["keywords"]
    assert "--tblite" in attributes["metadata"]["keywords"]


def test_bulk_static_detailed_input(tmpdir):
    tmpdir.chdir()

    atoms = bulk("Cu")
    atoms.calc = XTB(gfn={"method": 1})
    atoms.get_potential_energy()
    results = atoms.calc.results
    attributes = results["attributes"]
    assert results["energy"] == pytest.approx(-318.85844978148714)
    assert attributes["metadata"]["package"] == "xTB"
    assert attributes["metadata"]["coord_type"] == "POSCAR"
    assert attributes["scfenergies"] == results["energy"]
    assert "--gfn" not in attributes["metadata"]["keywords"]
    assert "--tblite" in attributes["metadata"]["keywords"]
