"""
Regression test for the bug where default values for positional-only arguments vanish.

This test verifies that the default values of positional-only arguments are properly
handled in signature parsing, specifically for syntax like:
.. py:function:: foo(a, b=0, /, c=1)

The issue was that default values for positional-only arguments were disappearing
after a fix was applied to the signature_from_str function. 
"""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_argument_defaults_preserved():
    """Test that default values for positional-only arguments are preserved."""
    # The key test case from the bug report - this should preserve defaults for positional-only args
    sig_str = "(a, b=0, /, c=1)"
    sig = signature_from_str(sig_str)
    
    # Should have 3 parameters
    assert len(sig.parameters) == 3
    
    # Get parameters by position  
    param_a, param_b, param_c = list(sig.parameters.values())
    
    # Check parameter a is positional-only with no default
    assert param_a.kind == inspect.Parameter.POSITIONAL_ONLY
    assert param_a.default == inspect.Parameter.empty
    
    # Check parameter b is positional-only with default value 0
    # This assertion detects the bug: positional-only default values were disappearing
    assert param_b.kind == inspect.Parameter.POSITIONAL_ONLY
    assert param_b.default == 0
    
    # Check parameter c is positional-only with default value 1
    assert param_c.kind == inspect.Parameter.POSITIONAL_ONLY
    assert param_c.default == 1


def test_positional_only_with_only_positional_defaults():
    """Test positional-only arguments with defaults but no keyword args.""" 
    sig_str = "(a, b=0, /, c=1)"
    sig = signature_from_str(sig_str)
    
    # Should have 3 parameters 
    assert len(sig.parameters) == 3
    
    # Verify all parameters are positional-only with correct defaults
    params = list(sig.parameters.values())
    
    # Parameter 'a' - positional-only, no default 
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default == inspect.Parameter.empty
    
    # Parameter 'b' - positional-only, default 0 (this is the bug case!)
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[1].default == 0
    
    # Parameter 'c' - positional-only, default 1
    assert params[2].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[2].default == 1


def test_positional_only_parameters_without_defaults():
    """Test that positional-only arguments without defaults work correctly."""
    sig_str = "(a, b, /, c)"
    sig = signature_from_str(sig_str)
    
    # Should have 3 parameters
    assert len(sig.parameters) == 3
    
    # Verify all parameters are positional-only with no defaults
    params = list(sig.parameters.values())
    
    # All should be positional-only with no defaults
    for i, param in enumerate(params):
        assert param.kind == inspect.Parameter.POSITIONAL_ONLY
        assert param.default == inspect.Parameter.empty