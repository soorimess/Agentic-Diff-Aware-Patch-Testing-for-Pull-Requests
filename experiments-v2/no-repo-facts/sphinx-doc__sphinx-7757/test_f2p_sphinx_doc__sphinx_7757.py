"""
Test for positional-only arguments with default values in signature_from_str.

This test reproduces the bug where default values for positional-only arguments
vanish in Sphinx's signature parsing.
"""

import pytest
from sphinx.util.inspect import signature_from_str
from inspect import Parameter


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults are handled correctly."""
    # This should work according to the bug report
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a (positional-only), b (positional-only with default), c (positional-or-keyword with default)
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default is Parameter.empty
    
    # Second parameter: b (positional-only, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'  # Should be '0', not Parameter.empty
    
    # Third parameter: c (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'  # Should be '1', not Parameter.empty


def test_positional_only_args_no_defaults():
    """Test positional-only arguments without defaults."""
    sig = signature_from_str('(a, b, /)')
    
    # Check parameters
    params = list(sig.parameters.values())
    
    # Should have 2 parameters: a, b (both positional-only, no defaults)
    assert len(params) == 2
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default is Parameter.empty
    
    # Second parameter: b (positional-only, no default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default is Parameter.empty


def test_mixed_args_simple():
    """Test mixed positional-only and regular arguments."""
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a (pos-only), b (pos-only with default), c (pos-or-key with default)
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default is Parameter.empty
    
    # Second parameter: b (positional-only, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'
    
    # Third parameter: c (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_regular_args_only():
    """Test regular arguments (no positional-only) to cover else branch."""
    sig = signature_from_str('(a, b=0, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a (pos-or-key), b (pos-or-key with default), c (pos-or-key with default)
    assert len(params) == 3
    
    # First parameter: a (positional-or-keyword, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[0].default is Parameter.empty
    
    # Second parameter: b (positional-or-keyword, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[1].default == '0'
    
    # Third parameter: c (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_positional_only_with_multiple_defaults():
    """Test multiple positional-only arguments with defaults."""
    sig = signature_from_str('(a=0, b=1, /, c=2)')
    
    # Check parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b (pos-only with defaults), c (pos-or-key with default)
    assert len(params) == 3
    
    # First parameter: a (positional-only, with default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == '0'
    
    # Second parameter: b (positional-only, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '1'
    
    # Third parameter: c (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '2'