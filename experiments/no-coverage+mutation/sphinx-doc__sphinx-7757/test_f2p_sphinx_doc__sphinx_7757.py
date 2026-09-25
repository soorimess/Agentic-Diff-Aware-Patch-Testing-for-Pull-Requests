"""
Regression test for sphinx-doc/sphinx#7757:
The default value for positional only argument has vanished
"""
from sphinx.util.inspect import signature_from_str


def test_bug_where_defaults_vanish():
    """
    Test that the bug exists where positional-only argument defaults vanish.
    
    Specifically, when parsing (a, b=0, /, c=1):
    - Parameter 'b' should have default=0 
    - But currently it has default=<class 'inspect._empty'>
    """
    # Parse the problematic signature
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Examine the result  
    params = list(sig.parameters.values())
    
    # This assertion will fail when the bug exists (which it does in current code)
    # It will pass once the fix is applied  
    b_default_value = params[1].default
    assert b_default_value == 0, f"Expected default=0 for b, but got {b_default_value}"