"""
Regression test for Symbol __dict__ behavior change.

The bug: In version 1.7, Symbol instances gained a __dict__ attribute when they 
should not have one (since they define __slots__ = ('name',)).

This test ensures that Symbol instances do NOT have __dict__ attribute, 
which is the correct behavior according to the __slots__ definition.
"""
from sympy import Symbol


def test_symbol_should_not_have_dict():
    """Test that Symbol instances should not have __dict__ attribute.
    
    This is the core bug: Symbol instances incorrectly have __dict__ when
    they should respect their __slots__ definition.
    """
    s = Symbol('s')
    
    # Symbol has __slots__ = ('name',), so it should not have __dict__
    # The bug is that __dict__ exists when it shouldn't
    try:
        # This should raise AttributeError in correct behavior
        dict_attr = s.__dict__
        # If we get here, __dict__ exists - this is the bug
        # The bug report shows this should raise AttributeError in 1.6.2
        raise AssertionError("__dict__ should not exist on Symbol instances with __slots__")
    except AttributeError:
        # This is the correct behavior - __dict__ should not exist
        pass