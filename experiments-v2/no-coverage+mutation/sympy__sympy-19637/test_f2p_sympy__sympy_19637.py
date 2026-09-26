from sympy.core.sympify import kernS

def test_kernS_no_unbound_local_error():
    """Test that kernS doesn't raise UnboundLocalError when kern variable is not defined"""
    # This specific case triggers the bug where kern is referenced before assignment
    # The bug happens when there's no space in the string but kern variable 
    # is referenced later without being defined
    text = "(2*x)/(x-1)"
    
    # This should not raise UnboundLocalError: local variable 'kern' referenced before assignment
    # The function should handle this gracefully
    try:
        expr = kernS(text)
        # If we get here without UnboundLocalError, the fix works
        assert expr is not None
    except UnboundLocalError as e:
        if "'kern' referenced before assignment" in str(e):
            raise AssertionError("UnboundLocalError still occurs: " + str(e))
        else:
            # Some other UnboundLocalError, re-raise
            raise
    except Exception:
        # Any other exception is fine - we're specifically testing for the UnboundLocalError
        pass