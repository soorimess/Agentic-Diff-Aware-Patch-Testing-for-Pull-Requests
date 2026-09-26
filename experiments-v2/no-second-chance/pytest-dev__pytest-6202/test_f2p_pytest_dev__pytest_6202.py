"""
Regression test for pytest-dev/pytest#6202

This test verifies that parameterized test names with dots and brackets
are displayed correctly in test reports without incorrect replacement
of ".[" with "[" in the test name.

The bug was in src/_pytest/python.py in the getmodpath method:
- Before fix: return s.replace(".[", "[")  # Incorrectly transforms "..[" to ".["
- After fix: return ".".join(parts)       # Preserves original string correctly
"""

import subprocess
import sys
import tempfile
import os


def test_parameterized_test_name_display():
    """
    Test that verifies the specific bug where "..[" parameter 
    gets incorrectly displayed as ".[" in test reports.
    
    This test creates a temporary test file and runs it to check
    the actual output format in the failure report.
    
    The test should pass when the bug is fixed (correct display) 
    and fail when the bug is present (incorrect display).
    """
    
    # Create a test file with the exact problematic case
    test_content = '''import pytest

@pytest.mark.parametrize("a", ["..["])
def test_boo(a):
    assert 0
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Run pytest on this file and capture output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            '-v', '--tb=short', 
            temp_file
        ], capture_output=True, text=True, cwd='.')
        
        # Check the output for the bug
        output = result.stdout + result.stderr
        
        # The bug manifests as: test_boo[.[] instead of test_boo[..[]
        # We need to look for the actual pattern in the output
        
        # Look for the specific failure line pattern
        lines = output.split('\n')
        failure_line = None
        for line in lines:
            if 'test_boo' in line and 'FAILED' not in line and '____' in line:
                failure_line = line
                break
        
        if failure_line:
            # Check if it contains the incorrect pattern
            if '[.[]' in failure_line:
                raise AssertionError("Bug present: test name incorrectly shows as .[ instead of ..[")
            elif '[..[]' in failure_line:
                # This is the correct behavior
                return  # Test passes
            else:
                raise AssertionError(f"Unexpected failure line format: {failure_line}")
        else:
            raise AssertionError(f"Could not find failure line in output: {output}")
            
    finally:
        # Clean up
        os.unlink(temp_file)