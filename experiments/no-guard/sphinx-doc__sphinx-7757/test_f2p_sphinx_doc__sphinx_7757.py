"""
Test for regression of positional-only argument default values

This covers the bug where default values for positional-only arguments 
were lost in Sphinx's signature parsing.
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_default_values():
    """
    Test that positional-only arguments with defaults are properly parsed.
    
    The original bug showed that for signature "(a, b=0, /, c=1)",
    parameter 'b' would show as 'b' instead of 'b=0' - i.e. default value missing.
    """
    # Test case from the bug report
    sig_str = "(a, b=0, /, c=1)"
    
    sig = signature_from_str(sig_str)
    
    # Debug: Print info to help understand what's happening
    params = list(sig.parameters.values())
    print(f"Signature: {sig}")
    for i, param in enumerate(params):
        print(f"  Param {i}: {param.name} - kind: {param.kind} - default: {param.default}")
    
    # The main assertion that will catch the bug
    # Parameter 'b' should have default value 0, not Parameter.empty
    assert len(params) == 3
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty  # a has no default 
    
    assert params[1].name == 'b'  # b is positional-only  
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == 0  # BUG: This should be 0 but is Parameter.empty
    
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == 1  # This one worked correctly