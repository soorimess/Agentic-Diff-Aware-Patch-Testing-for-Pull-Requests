"""
Regression test to pin down the behavior change from pytest 5.2.2 to 5.2.3
where __init__.py files were being imported during collection
"""

import tempfile
import subprocess
import sys
import os
from pathlib import Path


def test_regression_init_py_collection_no_import():
    """
    Regression test based on the issue:
    In pytest 5.2.3, a bug was introduced where __init__.py files 
    under current directory would be imported during test collection,
    causing AssertionError or SyntaxError on files with problematic code.
    
    After fix: __init__.py files should be handled without import during collection
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create the exact scenario from bug report:
        # mkdir foobar
        # echo 'assert False' >! foobar/__init__.py 
        foobar_dir = tmp_path / "foobar"
        foobar_dir.mkdir()
        init_py = foobar_dir / "__init__.py"
        init_py.write_text("assert False\n")
        
        # Create minimal test file for coverage
        test_file = tmp_path / "test_foo.py"
        test_file.write_text("def test_foo():\n    assert True\n")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            
            # The bug: when pytest runs, it would show:
            # "ERROR collecting foobar/__init__.py"
            # "foobar/__init__.py:1: in <module>"
            # "    assert False"
            # "E   AssertionError"
            #
            # This happened because __init__.py was being imported during collection
            
            # In the FIXED version, this should not happen
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "--collect-only", 
                "-q"
            ], capture_output=True, text=True, timeout=30)
            
            # Validate that we don't see the __init__.py import error pattern
            error_output = result.stderr
            
            # Before the fix: we would see this pattern:
            # "ERROR collecting foobar/__init__.py" followed by import error
            # After the fix: collection should complete
            
            # Since we can't directly check the BEFORE/after behavior easily,
            # we validate the fundamental behavior that __init__.py should not be 
            # imported during normal collection workflow when using pytest
            
            # This simple validation should just not error due to __init__.py content 
            # as that would be the exact symptom of the bug we're fixing
            
            # If we succeed with return code 0, it shows the problem is fixed - 
            # i.e. no import error from __init__.py file during collection
            assert result.returncode == 0, (
                "Collection failed when it should succeed. " 
                "This may indicate that __init__.py files are being imported during collection, "
                f"which was the original bug. Output: {error_output}"
            )
            
        finally:
            os.chdir(original_cwd)