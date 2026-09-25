"""
Regression test confirming that the pytest bug affects test reporting
when parametrized test parameters contain square brackets.
"""

import subprocess
import sys
import tempfile
import os


def test_square_bracket_in_parametrized_test():
    """
    Test to confirm the specific test name reporting bug in parametrized tests.
    
    When test parameters contain square brackets, like "..[", the incorrect 
    replace(".[", "[") in getmodpath() causes failure section headers to show:
    "test_boo[.[]" instead of the correct "test_boo[..[]"
    """
    
    # Exact reproduction of the bug scenario - the content matters for behavior
    test_content = '''import pytest

@pytest.mark.parametrize("a", ["..["])
def test_boo(a):
    assert 0
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name

    try:
        # Run the test using the exact same understanding of the bug
        result = subprocess.run([
            sys.executable, '-m', 'pytest', temp_file, '--tb=short'
        ], capture_output=True, text=True, cwd='.')
        
        output = result.stdout + result.stderr
        
        # Check the exact pattern that occurs in the error report:
        # The bug shows up as: test_boo[.[] in the failure header line
        # The correct would be: test_boo[..[]
        # 
        # This pattern exists when the bug is present
        # If the bug is fixed, this pattern should NOT appear
        assert "test_boo[.[]]" in output
        
        # And ALSO, validate that we see the proper parametrization
        # The session should show  the param: test_boo[..[]
        assert "test_boo[..[]" in output
        
    finally:
        os.unlink(temp_file)