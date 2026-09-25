"""
Regression test for Symbol __dict__ access issue.

The PR fixes the bug where Symbol instances unexpectedly gained __dict__ support
in version 1.7, causing them to have empty __dict__ when they shouldn't.

This test ensures Symbol instances properly respect __slots__ semantics 
and do not gain __dict__ access unexpectedly.
"""

from sympy import Symbol


def test_symbol_should_not_allow_dict_access():
    """
    Test that Symbol instances properly prevent __dict__ access.
    
    In the buggy behavior (before fix): Symbol.__dict__ was accessible returning {}
    In the fixed behavior (after fix): Symbol.__dict__ should raise AttributeError
    
    This test validates that the fix enforces correct __slots__ semantics.
    """
    s = Symbol('test')
    
    # Symbol should define __slots__ = ('name',)  
    assert hasattr(Symbol, '__slots__')
    assert Symbol.__slots__ == ('name',)
    
    # The main assertion: Symbol instances should NOT have __dict__ access
    # because they define __slots__ = ('name',) 
    try:
        _ = s.__dict__
        # If __dict__ is accessible, this is the buggy state that should not occur
        # The test FAILS in the buggy state because __dict__ exists when it shouldn't
        raise AssertionError(
            "Symbol instances should not allow __dict__ access (violates __slots__ semantics)")
    except AttributeError:
        # This is correct - Symbol instances should not allow __dict__ access 
        # because of their __slots__ definition
        pass


def test_symbol_slots_correct_behavior():
    """
    Test that Symbol correctly follows __slots__ semantics regarding __dict__ access.
    
    The core difference this test identifies:
    - Buggy state: Symbol.__dict__ works 
    - Fixed state: Symbol.__dict__ raises AttributeError
    """
    s = Symbol('s')
    
    # Verify the class definition is correct
    assert hasattr(s, '__slots__')
    assert s.__slots__ == ('name',)
    
    # This test will FAIL in buggy state but PASS in fixed state:
    # In buggy version, s.__dict__ succeeds (returning {})
    # In fixed version, s.__dict__ raises AttributeError
    try:
        # This access should be forbidden for Symbol instances with __slots__  
        dict_val = s.__dict__  
        # If this succeeds, we're in the buggy state and test fails appropriately
        raise AssertionError("Symbol instances with __slots__ should not allow __dict__ access")
    except AttributeError:
        # Expected behavior in fixed state
        pass