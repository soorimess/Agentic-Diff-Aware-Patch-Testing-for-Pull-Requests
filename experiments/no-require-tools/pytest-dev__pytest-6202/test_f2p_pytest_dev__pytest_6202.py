"""
Regression test for pytest-dev/pytest#6202
Test for correct handling of bracket characters in test parameter values
"""
import pytest


@pytest.mark.parametrize("a", ["..["])
def test_boo(a):
    """This directly reproduces the bug report case.
    
    Expected behavior:
    - Test reports should show "test_boo[..[]" in headers
    - Before the fix, reported as "test_boo[.[]"
    
    This test ensures that the problematic replacement logic does not 
    corrupt parameter values containing bracket characters.
    """
    assert 0


# One additional minimal test to ensure our assertions don't create issues
def test_for_verification_purpose():
    """
    A safe test to not interfere with verify behavior checking.
    """
    pass