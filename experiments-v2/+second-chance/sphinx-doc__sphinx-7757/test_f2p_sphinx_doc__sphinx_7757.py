"""
Regression test for sphinx-doc/sphinx#7757
The default value for positional only argument has vanished
"""
import pytest
from inspect import Parameter
from sphinx.util import inspect


def test_signature_from_str_positional_only_args_with_defaults():
    """Test that positional-only arguments with default values preserve their defaults."""
    # Test case with positional-only arguments that have defaults
    signature = '(a, b=0, /)'
    sig = inspect.signature_from_str(signature)
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 2
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Second parameter: b (positional-only, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'  # Should be '0', not Parameter.empty


def test_signature_from_str_positional_only_args_mixed_defaults():
    """Test case with positional-only args and regular args with defaults."""
    # Valid syntax: positional-only args first, then regular args
    signature = '(a, b=1, /, c=2)'
    sig = inspect.signature_from_str(signature)
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Second parameter: b (positional-only, with default)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '1'  # Should be '1', not Parameter.empty
    
    # Third parameter: c (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '2'  # Should be '2', not Parameter.empty


def test_signature_from_str_positional_only_all_defaults():
    """Test case where all positional-only args have defaults."""
    signature = '(a=1, b=2, /, c=3)'
    sig = inspect.signature_from_str(signature)
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # All should have defaults
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == '1'
    
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '2'
    
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '3'


def test_signature_from_str_no_positional_only_args_with_defaults():
    """Test case with no positional-only arguments but with defaults - exercises default handling logic."""
    # This tests the case where there are no positional-only args, but there are defaults
    # This exercises the logic that was broken in the old code
    signature = '(a, b=0, c=1)'
    sig = inspect.signature_from_str(signature)
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # All parameters should have proper defaults
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[0].default == Parameter.empty
    
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[1].default == '0'
    
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'