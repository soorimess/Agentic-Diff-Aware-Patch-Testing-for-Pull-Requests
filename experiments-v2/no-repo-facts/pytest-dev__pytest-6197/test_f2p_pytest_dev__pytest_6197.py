"""
Regression test for pytest bug: pytest tries to collect random __init__.py files
This test verifies that __init__.py files with failing code don't cause collection errors
in pytest 5.2.3+ (after the fix).
"""
import os
import tempfile
import subprocess
import sys


def test_init_py_collection_ignores_failing_init_files():
    """
    Test that __init__.py files with failing code are ignored during collection.
    
    This is a regression test for the bug where pytest 5.2.3 would try to import
    __init__.py files during collection, causing errors when those files contain
    code that fails to execute (like assert False).
    
    In the fixed version, __init__.py files should be ignored during collection
    and not cause import errors.
    """
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a foobar directory with an __init__.py that has failing code
        foobar_dir = os.path.join(tmpdir, "foobar")
        os.makedirs(foobar_dir)
        
        # Create __init__.py with failing assertion (this is the bug case)
        init_py_path = os.path.join(foobar_dir, "__init__.py")
        with open(init_py_path, "w") as f:
            f.write("assert False\n")
        
        # Create a simple test file in the parent directory
        test_file = os.path.join(tmpdir, "test_foo.py")
        with open(test_file, "w") as f:
            f.write("""
def test_something():
    assert True
""")
        
        # Change to the temp directory to run pytest
        old_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            
            # Run pytest and capture the result
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                "--collect-only",  # Just collect, don't run
                "-v"
            ], capture_output=True, text=True, timeout=30)
            
            # Check if the specific error about __init__.py import is present
            output = result.stdout + result.stderr
            
            # In the BUGGY version, we get an error about collecting foobar/__init__.py
            # In the FIXED version, the __init__.py should be ignored and not cause errors
            if "ERROR collecting foobar/__init__.py" in output and "AssertionError" in output:
                # This indicates the bug is present - pytest is trying to import __init__.py
                # This test should fail in the buggy version, which is what we want
                raise AssertionError("Bug reproduced: pytest is trying to import __init__.py during collection")
            
            # If we get here without the specific error, the collection succeeded
            # This means the __init__.py was properly ignored (fixed behavior)
            assert result.returncode == 0, f"Pytest collection failed with error:\n{output}"
            
        finally:
            os.chdir(old_cwd)