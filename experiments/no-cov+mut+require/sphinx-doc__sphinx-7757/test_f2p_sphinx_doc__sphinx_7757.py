"""
Test for issue sphinx-doc/sphinx#7757 - default value for positional only argument vanished
"""

from inspect import Parameter
from sphinx.util.inspect import signature_from_str


def test_positional_only_argument_defaults():
    """Test that default values are preserved for positional-only arguments."""
    # This signature replicates the original bug report example:
    # .. py:function:: foo(a, b=0, /, c=1)
    sig = signature_from_str('(a, b=0, /, c=1)')
    
    params = list(sig.parameters.values())
    
    # Should have 3 parameters: a, b, c
    assert len(params) == 3
    
    # Check parameter 'a' - positional-only without default
    assert params[0].name == 'a'
    assert params[0].kind == Parameter.POSITIONAL_ONLY
    assert params[0].default == Parameter.empty
    
    # Check parameter 'b' - positional-only WITH default (this was the bug)
    assert params[1].name == 'b'
    assert params[1].kind == Parameter.POSITIONAL_ONLY
    assert params[1].default == '0'  # Default should be '0', not Parameter.empty
    
    # Check parameter 'c' - keyword-or-positional WITH default 
    assert params[2].name == 'c'
    assert params[2].kind == Parameter.POSITIONAL_OR_KEYWORD
    assert params[2].default == '1'  # Default should be '1', not Parameter.empty