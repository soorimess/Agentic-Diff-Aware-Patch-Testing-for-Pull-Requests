"""
Regression test for sphinx-doc/sphinx#7757
The default value for positional only argument has vanished
"""
import pytest
from inspect import Parameter

from sphinx.util import inspect


def test_signature_from_str_positional_only_with_defaults():
    """Test that positional-only arguments retain their default values."""
    # Test the exact case from the bug report
    sig = inspect.signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # Check first parameter (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default is Parameter.empty
    
    # Check second parameter (positional-only, with default) - THIS IS THE BUG
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    # Verify that default value is properly set to 0
    # Before the fix, this would be Parameter.empty (the default value vanished)
    assert params[1].default == '0'
    
    # Check third parameter (positional-or-keyword, with default)
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_signature_from_str_positional_only_variations():
    """Test various combinations of positional-only arguments with defaults."""
    # Test all positional-only with defaults
    sig = inspect.signature_from_str('(a=1, b=2, /)')
    params = list(sig.parameters.values())
    assert len(params) == 2
    
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == '1'
    
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '2'
    
    # Test mixed positional-only and keyword args
    sig = inspect.signature_from_str('(a, b=2, /, c=3, d=4)')
    params = list(sig.parameters.values())
    assert len(params) == 4
    
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default is Parameter.empty
    
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '2'
    
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '3'
    
    assert params[3].name == 'd'
    assert params[3].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[3].default == '4'


if __name__ == '__main__':
    # These tests can be run directly for debugging
    test_signature_from_str_positional_only_with_defaults()
    test_signature_from_str_positional_only_variations()
    print("All tests passed!")