"""
Regression test for issue where default values for positional-only arguments vanish.

This test ensures that when parsing function signatures with positional-only arguments
that have default values (e.g., "foo(a, b=0, /, c=1)"), the default values are properly
preserved in the resulting Signature object.
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults preserve their default values."""
    # This is the case from the bug report
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b, c
    assert len(params) == 3
    
    # Parameter 'a' should be positional-only with no default
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Parameter 'b' should be positional-only with default 0
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == 0
    
    # Parameter 'c' should be positional-or-keyword with default 1
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == 1


def test_positional_only_args_no_defaults():
    """Test that positional-only arguments without defaults work correctly."""
    sig = signature_from_str('(a, b, /, c)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b, c
    assert len(params) == 3
    
    # All should be positional-only
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default is inspect.Parameter.empty
    
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default is inspect.Parameter.empty


def test_positional_only_args_simple_case():
    """Test simple case with just positional-only args with defaults."""
    sig = signature_from_str('(a, b=0, /)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 2 parameters: a, b
    assert len(params) == 2
    
    # Parameter 'a' should be positional-only with no default
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Parameter 'b' should be positional-only with default 0
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == 0