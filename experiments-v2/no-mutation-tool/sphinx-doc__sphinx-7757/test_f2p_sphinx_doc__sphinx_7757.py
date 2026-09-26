"""
Regression test for sphinx-doc/sphinx#7757
The default value for positional only argument has vanished
"""
import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_arguments_with_defaults():
    """Test that positional-only arguments with defaults preserve their default values.
    
    This test reproduces the bug described in sphinx-doc/sphinx#7757 where
    default values for positional-only arguments were not being shown.
    """
    # The exact case from the bug report: foo(a, b=0, /, c=1)
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a (positional-only), b (positional-only with default), c (positional-or-keyword with default)
    assert len(params) == 3
    
    # Check first parameter (a) - positional-only without default
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Check second parameter (b) - positional-only with default (this was the bug)
    # Before fix: params[1].default would be Parameter.empty
    # After fix: params[1].default should not be Parameter.empty
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    # The key assertion: this should NOT be empty (the bug was that it was empty)
    assert params[1].default is not inspect.Parameter.empty
    
    # Check third parameter (c) - positional-or-keyword with default
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default is not inspect.Parameter.empty


def test_positional_only_arguments_only():
    """Test positional-only arguments with defaults (simpler case)."""
    # Test a case with only positional-only arguments and defaults
    sig = signature_from_str('(a, b=0, /)')
    
    # Get the parameters
    params = list(sig.parameters.values())
    
    # Should have 2 parameters: a (positional-only), b (positional-only with default)
    assert len(params) == 2
    
    # Check first parameter (a) - positional-only without default
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Check second parameter (b) - positional-only with default (this was the bug)
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    # The key assertion: this should NOT be empty (the bug was that it was empty)
    assert params[1].default is not inspect.Parameter.empty