"""
Regression test for pytest issue where __init__.py files are being imported
during collection in version 5.2.3, causing failures when __init__.py files
contain code that can't be executed on certain platforms.
"""
import os
import pytest
from _pytest.main import ExitCode


def test_init_py_files_not_imported_during_collection(tmp_path):
    """
    Test that __init__.py files are not imported during collection.
    
    This is a regression test for pytest 5.2.3 where __init__.py files were being
    imported during collection, causing collection to fail if the __init__.py
    contained code that would fail during import.
    
    The fix should prevent __init__.py files from being imported during collection.
    """
    # Create a temporary directory structure
    test_dir = tmp_path / "test_package"
    test_dir.mkdir()
    
    # Create an __init__.py that would fail if imported (this should NOT be imported during collection)
    init_file = test_dir / "__init__.py"
    init_file.write_text("assert False  # This should not be executed during collection\n")
    
    # Create a regular test file that should pass
    test_file = test_dir / "test_something.py"
    test_file.write_text("""
def test_something():
    assert True
""")
    
    # Change to the test directory and run pytest
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        # This should succeed even though __init__.py contains failing code
        # because it should not be imported during collection
        result = pytest.main(["-v", str(test_dir)])
        # This assertion should pass when the fix is applied
        # It should fail when the bug exists (before the fix)
        assert result == ExitCode.OK, f"Collection failed with exit code {result}"
    finally:
        os.chdir(old_cwd)