"""
Regression test for positional-only arguments with default values.

This test ensures that default values for positional-only arguments
are properly displayed in Sphinx documentation.
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_argument_defaults():
    """Test that positional-only arguments with defaults show their default values."""
    # The bug: positional-only arguments with defaults lose their default values
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Parameter 'b' should have default value 0, not Parameter.empty
    # This is the core bug being tested
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == 0, f"Expected default 0, got {params[1].default}"


def test_positional_only_argument_no_defaults():
    """Test that positional-only arguments without defaults work correctly."""
    sig = signature_from_str('(a, b, /, c)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # All positional-only parameters should have no defaults
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default is inspect.Parameter.empty