"""
Regression test for pytest issue where test report headlines incorrectly
format parametrized arguments containing '[' character.

Bug report showed that ".[" was being incorrectly replaced with "[" in 
test report headlines, affecting parametrized tests with arguments 
containing brackets like "..[".

This test asserts that test names show correctly in failure reports:
- "test_boo[..[] " instead of "test_boo[.[] " 
"""

import subprocess
import sys
import tempfile
import os


def test_parametrized_test_names_with_brackets_show_correctly():
    """
    Test that parametrized test names containing bracket characters 
    display correctly in all parts of test report output.

    Before fix: "test_boo[..[] FAILED" and "test_boo[.[] " in error report
    After fix:  "test_boo[..[] FAILED" and "test_boo[..[] " in error report
    
    The bug was in src/_pytest/python.py line 289 where 
    'return s.replace(".[", "[")' caused test headlines to be corrupted.
    """
    # Create exactly the test case from the bug report
    test_content = '''
import pytest

@pytest.mark.parametrize("a", ["..["])
def test_boo(a):
    assert 0
'''
    
    # Write to temp file and run pytest on it
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Run pytest capturing full output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            temp_file, 
            '-v', '--tb=short'
        ], capture_output=True, text=True, cwd='.')
        
        output = result.stdout + result.stderr
        
        # The bug manifests in the detailed error report section
        # Check that we have correct format in both places:
        # 1. First line: "test_boo[..[] FAILED" 
        # 2. Error section: "test_boo[..[] " (the correct format)
        assert "test_boo[..[] " in output, (
            "Expected correct test name format not found in output. "
            f"Full output: {output}"
        )
        
        # Verify we don't have the buggy format in error section
        # The bug shows "test_boo[.[] " which should NOT appear in the report
        assert "test_boo[.[] " not in output or output.count("test_boo[.[] ") == 0, (
            "Bug still present: found corrupted test name format. "
            f"Full output: {output}"
        )
        
    finally:
        os.unlink(temp_file)