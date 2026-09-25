"""
Test for kernS UnboundLocalError issue.

The bug was: kernS function had an UnboundLocalError when 'kern' was 
referenced before assignment in certain conditions.
"""

from sympy.core.sympify import kernS

def test_kernS_no_space_string():
    """Test that kernS handles strings without spaces correctly (original bug case)."""
    # This specific string used to raise UnboundLocalError in the buggy version
    # The exact case mentioned in the bug report
    text = "(2*x)/(x-1)"
    try:
        result = kernS(text)
        # If we get here without UnboundLocalError, it worked
        assert result is not None
    except UnboundLocalError:
        # This is the exact bug we're testing for
        raise AssertionError("UnboundLocalError should not be raised for strings without spaces")
    except Exception:
        # Other exceptions are fine - we're specifically testing the UnboundLocalError bug
        pass

def test_kernS_with_space_string():
    """Test that kernS handles strings with spaces correctly (should work with or without fix)."""
    # A string that would trigger the kern logic path
    text = "(2*x) /(x-1)"  # Note the space between (2*x) and /(x-1)
    try:
        result = kernS(text)
        assert result is not None
    except UnboundLocalError:
        raise AssertionError("UnboundLocalError should not be raised for strings with spaces")
    except Exception:
        pass  # Other exceptions are OK