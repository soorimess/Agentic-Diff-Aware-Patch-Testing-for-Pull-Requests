"""Test for the issue where positional-only argument default values vanish."""

import inspect
from sphinx.util.inspect import signature_from_str


def test_positional_only_arg_default_values_bug():
    """Test that demonstrates the bug where positional-only arg defaults are lost.
    
    This tests specifically the case from the bug report:
    .. py:function:: foo(a, b=0, /, c=1)
    
    Parameter 'b' should have default value 0, but was showing Parameter.empty
    """
    # Parse a signature with positional-only args with defaults
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b, c
    assert len(params) == 3
    
    # Parameter 'a' - positional-only, no default 
    assert params[0].kind == inspect.Parameter.POSITIONAL_ONLY
    assert params[0].default == inspect.Parameter.empty
    
    # Parameter 'b' - positional-only, default 0 (this was the bug)
    assert params[1].kind == inspect.Parameter.POSITIONAL_ONLY
    # This assertion should pass after fix but fails in buggy code:
    assert params[1].default == 0
    
    # Parameter 'c' - positional-or-keyword, default 1 (this works correctly)
    assert params[2].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == 1