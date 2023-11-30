import pytest

from xtb_ase.io import read_xtb


def test_bad_read(tmpdir):
    tmpdir.chdir()
    with pytest.raises(RuntimeError):
        read_xtb("bad_file_name")
