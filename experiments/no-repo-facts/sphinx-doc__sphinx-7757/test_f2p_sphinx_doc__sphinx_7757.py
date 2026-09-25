"""Test for issue with default values in positional-only arguments"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults show their defaults correctly."""
    # This is the specific case from the bug report
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # Check first parameter (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Check second parameter (positional-only, has default)
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'
    
    # Check third parameter (positional-or-keyword, has default)
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_positional_only_args_with_defaults_legacy_pattern():
    """Test that positional-only args with defaults work correctly - another pattern."""
    # A few more edge cases to really test the behavior
    sig = signature_from_str('(a=1, /)')
    
    # Check parameters
    params = list(sig.parameters.values())
    assert len(params) == 1
    
    # Check first parameter (positional-only, has default)  
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default == '1'