"""
Test for regression where pytest 5.2.3 tries to collect random __init__.py files.
This test directly tests the behavior described in the bug report: 
pytest should not be importing __init__.py files during collection.
"""

import tempfile
import subprocess
import sys
from pathlib import Path


def test_init_py_files_dont_cause_import_errors():
    """
    Test that when pytest encounters an __init__.py file with failing code,
    it should not cause collection to fail because it tries to import the __init__.py.
    
    Before fix: Collection would fail with "ERROR collecting __init__.py"
    After fix: Collection should succeed
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create the problematic __init__.py exactly as described in the bug report
        init_file = temp_path / "__init__.py"
        init_file.write_text("assert False")
        
        # Add a proper test file
        test_file = temp_path / "test_foo.py"
        test_file.write_text("def test_foo():\n    assert True\n")
        
        # Run pytest collection
        result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--collect-only",
                str(temp_path)
            ], capture_output=True, text=True, cwd=temp_dir)
            
        # The key assertion: we should NOT see an error from trying to collect the __init__.py
        # Error message should NOT contain "ERROR collecting __init__.py"
        error_output = result.stderr + result.stdout
        assert "ERROR collecting __init__.py" not in error_output, (
            "Pytest incorrectly tried to import and collect __init__.py during collection!\n"
            f"Error output: {error_output}"
        )
        
        # Collection should have at least found our test file
        assert "test_foo" in error_output or result.returncode == 0, (
            "Collection failed unexpectedly - the __init__.py import error may be hiding real problems"
        )         


def test_collect_without_init_py_import_error():
    """
    Specific test ensuring collection doesn't fail due to __init__.py import attempt.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create failing __init__.py 
        init_file = temp_path / "__init__.py"
        init_file.write_text("assert False  # This should never be executed during collection")
        
        # Create a valid test file
        test_file = temp_path / "test_normal.py"
        test_file.write_text("def test_something():\n    assert True\n")
        
        # Run collection with verbose output
        result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--collect-only", 
                "-v",
                str(temp_dir)
            ], capture_output=True, text=True, cwd=temp_dir)
            
        # In the broken version we would get:
        # ERROR collecting __init__.py
        # __init__.py:1: in <module>
        #    assert False  
        # E   AssertionError
        
        # Confirm that we don't have these specific error messages
        error_output = result.stdout + result.stderr
        # The bug manifests as these specific lines in error output that should not be present
        lines = error_output.split('\n')
        init_errors = [line for line in lines if 'ERROR collecting __init__.py' in line]
        assert len(init_errors) == 0, (
            "Found __init__.py collection errors when there should be none - bug reproduced.\n"
            f"Error lines: {init_errors}"
        )