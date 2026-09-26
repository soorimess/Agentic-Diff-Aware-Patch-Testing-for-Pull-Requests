"""
Regression test for sphinx-doc/sphinx#7757
Test that positional-only arguments with default values are handled correctly.
"""
import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_args_with_defaults():
    """Test that positional-only arguments with default values show their defaults."""
    # Test the exact case from the bug report: foo(a, b=0, /, c=1)
    # But since that would be invalid syntax (non-default follows default),
    # we test a valid case: foo(a, b=0, /)
    sig = signature_from_str('(a, b=0, /)')
    
    # Check that parameters are correctly identified
    params = list(sig.parameters.values())
    assert len(params) == 2
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Second parameter: b (positional-only, with default 0)
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'  # This should NOT be Parameter.empty


def test_positional_only_args_mixed_with_regular():
    """Test positional-only args mixed with regular args."""
    # Test a case with both positional-only and regular args with defaults
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # First parameter: a (positional-only, no default)
    assert params[0].name == 'a'
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default is inspect.Parameter.empty
    
    # Second parameter: b (positional-only, with default 0)
    assert params[1].name == 'b'
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'
    
    # Third parameter: c (positional-or-keyword, with default 1)
    assert params[2].name == 'c'
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'


def test_positional_only_args_without_defaults():
    """Test that positional-only arguments without defaults work correctly."""
    sig = signature_from_str('(a, b, /, c)')
    
    # Check that parameters are correctly identified
    params = list(sig.parameters.values())
    assert len(params) == 3
    
    # All should have no defaults
    for i, param in enumerate(params):
        assert param.default is inspect.Parameter.empty