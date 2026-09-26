"""Regression test for issue where default values for positional-only arguments vanish."""

from inspect import Parameter
from sphinx.util import inspect


def test_signature_from_str_positional_only_default_values():
    """Test that default values are preserved for positional-only arguments."""
    # This signature has default values for positional-only arguments
    signature = '(a, b=0, /, c=1)'
    sig = inspect.signature_from_str(signature)
    
    # Check that parameters are correctly parsed
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Check that 'a' is positional-only with no default
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['a'].default == Parameter.empty
    
    # Check that 'b' is positional-only with default value 0
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].default == '0'
    
    # Check that 'c' is positional-or-keyword with default value 1
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].default == '1'


def test_signature_from_str_positional_only_with_defaults():
    """Test positional-only arguments with defaults in various combinations."""
    # Test case from the bug report
    signature = '(a, b=0, /, c=1)'
    sig = inspect.signature_from_str(signature)
    
    # Check parameter kinds
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    
    # Check default values - this is the core of the bug
    # 'a' has no default (should be Parameter.empty)
    assert sig.parameters['a'].default == Parameter.empty
    
    # 'b' should have default value 0 (this was the bug - it was returning Parameter.empty)
    assert sig.parameters['b'].default == '0'
    
    # 'c' should have default value 1
    assert sig.parameters['c'].default == '1'


def test_signature_from_str_regular_args_only():
    """Test that regular arguments still work correctly (regression test)."""
    signature = '(a, b=0, c=1)'
    sig = inspect.signature_from_str(signature)
    
    # Check that parameters are correctly parsed
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Check that 'a' is positional-or-keyword with no default
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['a'].default == Parameter.empty
    
    # Check that 'b' is positional-or-keyword with default value 0
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['b'].default == '0'
    
    # Check that 'c' is positional-or-keyword with default value 1
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].default == '1'