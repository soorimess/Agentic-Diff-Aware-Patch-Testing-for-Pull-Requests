"""
Regression test for pytest 5.2.3 bug:
pytest tries to collect random __init__.py files
"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path


def test_init_py_in_subdirectory_not_imported_during_collection():
    """
    Regression test for pytest 5.2.3: when there's an __init__.py file in a 
    subdirectory that cannot be imported (due to assert False or syntax error),
    pytest tries to import it during collection, causing collection to fail.
    
    This test would fail on pytest 5.2.3 (and earlier) but should pass on 5.2.4+.
    """
    # Use temporary directory to isolate test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Create directory structure that matches bug report
        foobar_dir = tmpdir_path / "foobar"
        foobar_dir.mkdir()
        
        # Create a problematic __init__.py file that will fail on import 
        init_file = foobar_dir / "__init__.py"
        init_file.write_text("assert False\n") 
        
        # Create a legitimate test file - needed to trigger collection
        test_file = tmpdir_path / "test_foo.py" 
        test_file.write_text("def test_something():\n    assert True\n")
        
        # Run pytest from the temp directory 
        old_cwd = os.getcwd()
        try:
            os.chdir(tmpdir_path)
            
            # Run the collection phase - this should succeed (not fail with error code 2)
            # If the bug exists, it will fail at "ERROR collecting foobar/__init__.py"
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "--collect-only",
                "-q"
            ], capture_output=True, text=True, timeout=30)
            
            # After fix: return code 0 (success) - __init__.py not imported during collection
            # Before fix: return code 2 (error) - __init__.py was collected and imported  
            assert result.returncode != 2, (
                "Collection failed during __init__.py import - this indicates the bug exists.\n"
                f"Error details: {result.stderr}"
            )
            
        finally:
            os.chdir(old_cwd)