"""
Regression tests for Symbol __dict__ behavior bug.

The test ensures Symbol instances behave correctly with respect to __dict__.
In versions before 1.7, Symbol instances correctly did NOT have __dict__ attribute.
In version 1.7+, due to a bug in Printable class, Symbol instances incorrectly got __dict__.

This test should pass with the fix applied, and will fail with current buggy code.
"""

from sympy import Symbol

def test_symbol_should_not_have_dict_attribute():
    """
    Test that Symbol instances do not have __dict__ attribute.
    
    This is a regression test for the bug where Symbol instances
    incorrectly had __dict__ attribute due to Printable.__slots__ 
    being absent, and thus inheritance led to __dict__ creation.
    """
    s = Symbol('s')
    
    # Symbol instances should NOT have __dict__ attribute because:
    # 1. Symbol class defines __slots__ = ('name',)  
    # 2. This should prevent __dict__ from being created for instances
    # 3. If __dict__ exists, it's a bug introduced by the inheritance model
    try:
        # If __dict__ attribute exists, it's the buggy behavior
        _ = s.__dict__
        # If we get here, that means buggy __dict__ exists - this should fail
        assert False, "Symbol instances should not have __dict__ attribute (bug)"
    except AttributeError:
        # This is the correct behavior - Symbol should not have __dict__
        pass

def test_symbol_has_only_expected_slots():
    """Test that Symbol respects its __slots__ definition."""
    s = Symbol('s')
    
    # Symbol should only be able to have 'name' attribute as defined by __slots__
    assert hasattr(s, 'name')
    assert s.name == 's'
    
    # Symbol should NOT be able to have arbitrary attributes (since __slots__ is used)
    # This test mainly checks inheritance works correctly
    assert not hasattr(s, '__dict__')

def test_symbol_accepts_normal_operations():
    """Test that Symbol still works normally for core functionality."""
    s = Symbol('s')
    assert str(s) == 's'
    assert s.name == 's'