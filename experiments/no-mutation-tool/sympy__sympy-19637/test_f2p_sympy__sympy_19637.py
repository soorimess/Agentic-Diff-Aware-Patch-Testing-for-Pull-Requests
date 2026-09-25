"""Test for the kernS bug: 'kern' referenced before assignment"""

from sympy.core.sympify import kernS

def test_kernS_unbound_local_error():
    """Test that reproduces the UnboundLocalError in kernS when no spaces exist"""
    # This is the exact case from the bug report
    text = "(2*x)/(x-1)"
    # This should raise UnboundLocalError: local variable 'kern' referenced before assignment  
    try:
        expr = kernS(text)
        # If no exception occurs, it means the bug is fixed
        assert expr is not None
    except UnboundLocalError as e:
        # This is the error we want to make sure we catch if bug exists
        assert "kern" in str(e)
        raise