"""Regression test for positional-only argument default values issue.

This test verifies that the default values for positional-only arguments 
are correctly preserved in function signatures, particularly when they are 
followed by other parameters with default values.
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_default_values():
    """Test that positional-only arguments with default values are handled correctly."""
    # This reproduces the bug where default values for positional-only args vanish
    sig = signature_from_str('foo(a, b=0, /, c=1)')
    
    # Get the parameters 
    params = list(sig.parameters.values())
    
    # Check that we have the right number of parameters
    assert len(params) == 3
    
    # Check first parameter (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default == inspect.Parameter.empty
    
    # Check second parameter (positional-only, has default) - THIS IS THE BUG
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    # This is the critical assertion that was failing - the default should be 0
    assert params[1].default == 0
    
    # Check third parameter (positional-or-keyword, has default)
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == 1