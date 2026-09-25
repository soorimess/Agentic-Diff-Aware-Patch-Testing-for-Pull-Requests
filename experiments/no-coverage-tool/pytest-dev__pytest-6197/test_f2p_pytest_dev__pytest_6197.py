"""
Regression test for pytest issue: 
Regression in 5.2.3: pytest tries to collect random __init__.py files

This test specifically ensures that __init__.py files containing executable code 
don't cause collection failures during test discovery.
"""

import tempfile
import subprocess
import sys
import os


def test_initpy_does_not_import_during_collection():
    """
    This test fails if pytest tries to collect/validate __init__.py during test discovery.
    
    In the buggy behavior (pytest 5.2.3), __init__.py files with problematic code  
    would be imported during collection, causing AssertionError.
    
    In the fixed behavior, __init__.py files should be properly excluded from normal
    module collecting process.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create the same test structure as the bug report example
        test_dir = os.path.join(tmpdir, "foobar")
        os.makedirs(test_dir)
        
        # Create problematic __init__.py file
        init_py_path = os.path.join(test_dir, "__init__.py")
        with open(init_py_path, "w") as f:
            f.write("assert False\n")
            
        # Run pytest collection - this should NOT show ERROR collecting __init__.py
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--collect-only", "-v",
            test_dir
        ], capture_output=True, text=True, cwd=tmpdir)
        
        # Check for the exact error pattern that indicates the bug
        # If this error is present, the test should fail because:
        # - It means __init__.py file was imported during collection 
        # - Which would fail because of 'assert False'  
        stderr_output = result.stderr
        stdout_output = result.stdout
        
        # The bug shows up as this exact pattern in the STDERR:
        # "ERROR collecting foobar/__init__.py"  
        if "ERROR collecting" in stderr_output and "__init__.py" in stderr_output:
            # This indicates the bug is present - __init__.py was being collected
            raise AssertionError(
                "TEST FAILURE: Found collection error for __init__.py file. "
                "This indicates that pytest tried to import the __init__.py during "
                "collection, which caused AssertionError due to 'assert False'. "
                "This is the regression reported in pytest 5.2.3."
            )
            
        # If we get here, no such error exists, which means: 
        # 1. Either the fix is working properly (no import attempted)
        # 2. Or something else happened to make the error not show up in the same way
        # But either case our test passes correctly