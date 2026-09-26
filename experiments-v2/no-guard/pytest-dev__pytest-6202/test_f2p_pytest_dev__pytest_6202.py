"""
Regression test for pytest issue where '.[' is incorrectly replaced with '['
in test report headlines.

This test ensures that parameterized test names preserve '.[' characters
in parameter values correctly.
"""

import subprocess
import sys
import tempfile
import os


def test_parameterized_test_preserves_dot_bracket_in_names():
    """
    Test that parameter values containing '.[' are preserved in test names.
    
    The bug was in getmodpath() method where:
    - Old: return s.replace(".[", "[")  # Incorrectly modifies parameter values
    - New: return ".".join(parts)      # Preserves parameter values exactly
    
    This test ensures that legitimate '.[' characters in parameter values
    are not incorrectly converted to '[' in test report names.
    """
    # Test case from the bug report
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
        # Run pytest and capture output
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            '-v', '--tb=no',
            temp_file
        ], capture_output=True, text=True, cwd='.')
        
        # Get the output
        output = result.stdout + result.stderr
        
        # The key assertion: verify that we don't see the buggy replacement
        # If the bug is present, we'd see "test_boo[.[]" instead of "test_boo[..[]"
        assert "test_boo[.[]" not in output, (
            "BUG: '.[' was incorrectly replaced with '[' in test name. "
            "This indicates the replacement logic is still active and buggy. "
            "Expected 'test_boo[..[]' but found 'test_boo[.[]' in output."
        )
        
        # Verify correct behavior is present
        assert "test_boo[..[]" in output, (
            "Expected parameter value '..[' to be preserved in test name. "
            "The replacement logic should not affect legitimate '.[' characters."
        )
        
    finally:
        # Clean up
        os.unlink(temp_file)