"""
Regression test for sphinx-doc/sphinx#7757
Tests that default values for positional-only arguments are preserved.
"""

import pytest
from inspect import Parameter
from sphinx.util.inspect import signature_from_str


def test_positional_only_default_values():
    """Test that default values for positional-only arguments are preserved."""
    # This is the case from the bug report: foo(a, b=0, /, c=1)
    # The default value for b (positional-only) should be preserved
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Second parameter: b (positional-only, with default 0)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    # This is the bug: the default value should be '0' but is Parameter.empty
    assert params[1].default == '0'  # This should pass after fix, fail before
    
    # Third parameter: c (positional-or-keyword, with default 1)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_positional_only_with_defaults():
    """Test positional-only arguments with defaults."""
    sig = signature_from_str('(a, b=0, /)')
    
    params = list(sig.parameters.values())
    assert len(params) == 2
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Second parameter: b (positional-only, with default 0)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'


def test_mixed_positional_only_and_regular():
    """Test mixed positional-only and regular positional arguments with defaults."""
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Second parameter: b (positional-only, with default 0)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'
    
    # Third parameter: c (positional-or-keyword, with default 1)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'