import os
import tempfile
from pathlib import Path

from deq_eid.helpers import convert_to_int, zip_fgdb


def test_convert_to_int_with_valid_string():
    assert convert_to_int("123") == 123


def test_convert_to_int_with_invalid_string():
    assert convert_to_int("abc") == -1


def test_convert_to_int_with_none():
    assert convert_to_int(None) is None


def test_convert_to_int_with_empty_string():
    assert convert_to_int("") == -1


def test_zip_fgdb_with_valid_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        fgdb_path = temp_dir / "fgdb"
        os.makedirs(fgdb_path)

        # Create some dummy files
        file1 = fgdb_path / "file1.txt"
        file2 = fgdb_path / "file2.txt"
        with open(file1, "w") as f:
            f.write("File 1")
        with open(file2, "w") as f:
            f.write("File 2")

        zip_file_path = temp_dir / "fgdb.zip"

        zip_fgdb(fgdb_path, zip_file_path)

        assert os.path.exists(zip_file_path)
        assert os.path.isfile(zip_file_path)


def test_zip_fgdb_with_invalid_path():
    fgdb_path = "/path/to/nonexistent/fgdb"
    zip_file_path = "/path/to/zip/file.zip"

    try:
        zip_fgdb(fgdb_path, zip_file_path)
    except FileNotFoundError:
        pass
    else:
        assert False, "Function did not raise FileNotFoundError"
