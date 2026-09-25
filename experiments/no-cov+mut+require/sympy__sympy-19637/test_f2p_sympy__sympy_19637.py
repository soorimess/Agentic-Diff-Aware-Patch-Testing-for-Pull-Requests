from sympy.core.sympify import kernS

def test_kernS_unboundlocalerror():
    """Test that kernS doesn't raise UnboundLocalError with strings containing no spaces"""
    # Test the exact case that triggers the bug described in the issue
    text = "(2*x)/(x-1)"
    # This should not raise UnboundLocalError in the fixed version
    # The primary behavior this tests is: no exception raised
    try:
        expr = kernS(text)
        # This should work without UnboundLocalError
        assert expr is not None
    except UnboundLocalError:
        # This is the bug - should be fixed
        raise AssertionError("UnboundLocalError: local variable 'kern' referenced before assignment")