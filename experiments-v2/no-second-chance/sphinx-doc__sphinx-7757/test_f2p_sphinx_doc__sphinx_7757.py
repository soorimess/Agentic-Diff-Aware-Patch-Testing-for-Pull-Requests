"""
Regression test for sphinx-doc/sphinx#7757
Test that default values for positional-only arguments are preserved.
"""

import pytest
from inspect import Parameter
from sphinx.util.inspect import signature_from_str


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults are handled correctly."""
    # This signature has positional-only arguments with defaults
    # foo(a, b=0, /, c=1)
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Check that we have the right number of parameters
    assert len(sig.parameters) == 3
    
    # Get parameters by position
    param_a = sig.parameters['a']
    param_b = sig.parameters['b']
    param_c = sig.parameters['c']
    
    # Parameter 'a' should be positional-only without default
    assert param_a.kind == Parameter.POSITIONAL_ONLY
    assert param_a.default is Parameter.empty
    
    # Parameter 'b' should be positional-only WITH default
    assert param_b.kind == Parameter.POSITIONAL_ONLY
    assert param_b.default == '0'  # Should be string representation of default
    
    # Parameter 'c' should be positional-or-keyword WITH default
    assert param_c.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert param_c.default == '1'  # Should be string representation of default


def test_positional_only_args_without_defaults():
    """Test that positional-only arguments without defaults work correctly."""
    # This signature has positional-only arguments without defaults
    # foo(a, b, /, c=1)
    sig = signature_from_str('(a, b, /, c=1)')
    
    # Check that we have the right number of parameters
    assert len(sig.parameters) == 3
    
    # Get parameters by position
    param_a = sig.parameters['a']
    param_b = sig.parameters['b']
    param_c = sig.parameters['c']
    
    # Parameter 'a' should be positional-only without default
    assert param_a.kind == Parameter.POSITIONAL_ONLY
    assert param_a.default is Parameter.empty
    
    # Parameter 'b' should be positional-only without default
    assert param_b.kind == Parameter.POSITIONAL_ONLY
    assert param_b.default is Parameter.empty
    
    # Parameter 'c' should be positional-or-keyword WITH default
    assert param_c.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert param_c.default == '1'


def test_only_positional_only_args():
    """Test positional-only arguments without regular parameters."""
    # This signature has only positional-only arguments with defaults
    # foo(a, b=0, /)
    sig = signature_from_str('(a, b=0, /)')
    
    # Check that we have the right number of parameters
    assert len(sig.parameters) == 2
    
    # Get parameters by position
    param_a = sig.parameters['a']
    param_b = sig.parameters['b']
    
    # Parameter 'a' should be positional-only without default
    assert param_a.kind == Parameter.POSITIONAL_ONLY
    assert param_a.default is Parameter.empty
    
    # Parameter 'b' should be positional-only WITH default
    assert param_b.kind == Parameter.POSITIONAL_ONLY
    assert param_b.default == '0'


def test_regular_args_only():
    """Test regular arguments without positional-only (to cover else branch)."""
    # This signature has only regular arguments with defaults
    # foo(a, b=0, c=1)
    sig = signature_from_str('(a, b=0, c=1)')
    
    # Check that we have the right number of parameters
    assert len(sig.parameters) == 3
    
    # Get parameters by position
    param_a = sig.parameters['a']
    param_b = sig.parameters['b']
    param_c = sig.parameters['c']
    
    # Parameter 'a' should be positional-or-keyword without default
    assert param_a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert param_a.default is Parameter.empty
    
    # Parameter 'b' should be positional-or-keyword WITH default
    assert param_b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert param_b.default == '0'
    
    # Parameter 'c' should be positional-or-keyword WITH default
    assert param_c.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert param_c.default == '1'