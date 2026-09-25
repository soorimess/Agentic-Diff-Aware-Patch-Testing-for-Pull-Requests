"""
Regression test for position-only argument default values bug.

This test verifies that default values for positional-only arguments 
are properly preserved in Python 3.8+ signatures.
"""

import sys
from inspect import Parameter

import pytest

from sphinx.util import inspect


@pytest.mark.skipif(sys.version_info < (3, 8),
                    reason='python-3.8 or above is required')
def test_positional_only_args_with_defaults():
    """Test positional-only arguments with default values are preserved."""
    # This should not raise and should preserve all default values
    sig = inspect.signature_from_str('(a, b=0, /, c=1)')
    
    # Check parameters
    assert list(sig.parameters.keys()) == ['a', 'b', 'c']
    
    # Parameter 'a' should be POSITIONAL_ONLY with no default
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['a'].default is Parameter.empty
    
    # Parameter 'b' should be POSITIONAL_ONLY with default 0
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].default == '0'
    
    # Parameter 'c' should be POSITIONAL_OR_KEYWORD with default 1  
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].default == '1'


@pytest.mark.skipif(sys.version_info < (3, 8),
                    reason='python-3.8 or above is required')  
def test_positional_only_all_defaults():
    """Test all positional-only args with defaults."""
    sig = inspect.signature_from_str('(a=1, b=2, /, c=3)')
    
    # Parameter 'a' should be POSITIONAL_ONLY with default 1
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['a'].default == '1'
    
    # Parameter 'b' should be POSITIONAL_ONLY with default 2
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].default == '2'
    
    # Parameter 'c' should be POSITIONAL_OR_KEYWORD with default 3
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].default == '3'


@pytest.mark.skipif(sys.version_info < (3, 8),
                    reason='python-3.8 or above is required')
def test_mixed_positional_and_positional_only_defaults():
    """Test mixed positional-only and regular positional args with defaults."""
    sig = inspect.signature_from_str('(a, b=10, /, c=20)')
    
    # Parameter 'a' should be POSITIONAL_ONLY with no default
    assert sig.parameters['a'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['a'].default is Parameter.empty
    
    # Parameter 'b' should be POSITIONAL_ONLY with default 10
    assert sig.parameters['b'].kind == Parameter.POSITIONAL_ONLY
    assert sig.parameters['b'].default == '10'
    
    # Parameter 'c' should be POSITIONAL_OR_KEYWORD with default 20
    assert sig.parameters['c'].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters['c'].default == '20'