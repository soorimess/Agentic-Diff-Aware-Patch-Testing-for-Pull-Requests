"""
Regression test for sphinx-doc/sphinx#7757
The default value for positional only argument has vanished
"""

import pytest
from inspect import Parameter
from sphinx.util import inspect


def test_signature_from_str_positional_only_args_with_defaults():
    """Test that positional-only arguments with defaults show their default values."""
    # This is the test case from the bug report
    sig = inspect.signature_from_str('(a, b=0, /, c=1)')
    
    # Check that we have the right parameters
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Check parameter kinds
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY  # This was the bug - was POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    
    # Check that b has default value '0' (as string, not integer)
    # This was the bug - was Parameter.empty
    assert sig.parameters['b'].default == '0'
    
    # Check that c has default value '1'
    assert sig.parameters['c'].default == '1'


def test_signature_from_str_positional_only_args_mixed_defaults():
    """Test positional-only args with and without defaults."""
    sig = inspect.signature_from_str('(a, b, c=3, /, d=4)')
    
    # Check that we have the right parameters
    assert list(sig.parameters.keys()) == ['a', 'b', 'c', 'd']
    
    # Check parameter kinds
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_ONLY  # This was the bug - was POSITIONAL_OR_KEYWORD
    assert sig.parameters['d'].kind == Parameter.POSITIONAL_OR_KEYWORD
    
    # Check that c has default value '3' 
    # This was the bug - was Parameter.empty
    assert sig.parameters['c'].default == '3'
    
    # Check that d has default value '4'
    assert sig.parameters['d'].default == '4'
    
    # Check that a and b have no defaults
    assert sig.parameters['a'].default is Parameter.empty
    assert sig.parameters['b'].default is Parameter.empty


def test_signature_from_str_positional_only_args_all_defaults():
    """Test positional-only args all with defaults."""
    sig = inspect.signature_from_str('(a=1, b=2, /, c=3)')
    
    # Check that we have the right parameters
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Check parameter kinds
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    
    # Check that all have default values (as strings)
    assert sig.parameters['a'].default == '1'
    assert sig.parameters['b'].default == '2'
    assert sig.parameters['c'].default == '3'


def test_signature_from_str_regular_args_with_defaults():
    """Test that regular arguments with defaults still work (no positional-only args)."""
    sig = inspect.signature_from_str('(a, b=0, c=1)')
    
    # Check that we have the right parameters
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Check parameter kinds
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    
    # Check that b and c have default values
    assert sig.parameters['b'].default == '0'
    assert sig.parameters['c'].default == '1'


def test_signature_from_str_no_args():
    """Test function with no arguments."""
    sig = inspect.signature_from_str('()')
    
    # Check that we have the right parameters
    assert list(sig.parameters.keys()) == []
    
    # Check return annotation is empty
    assert sig.return_annotation is Parameter.empty