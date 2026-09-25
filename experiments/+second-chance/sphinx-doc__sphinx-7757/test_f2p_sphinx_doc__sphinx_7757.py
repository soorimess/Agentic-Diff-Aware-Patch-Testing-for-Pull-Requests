"""
Regression test for positional-only argument default values issue.

This test ensures that default values for positional-only arguments are properly
handled in the signature_from_str function.
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults are properly parsed."""
    # Test case from the bug report: foo(a, b=0, /, c=1)
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b, c
    assert len(params) == 3
    
    # Parameter 'a' should be POSITIONAL_ONLY with no default
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Parameter 'b' should be POSITIONAL_ONLY with default value 0
    # This is what fails - the default value is not properly set
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    # This assertion should pass after the fix:
    assert params[1].default == 0
    
    # Parameter 'c' should be POSITIONAL_OR_KEYWORD with default value 1
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == 1