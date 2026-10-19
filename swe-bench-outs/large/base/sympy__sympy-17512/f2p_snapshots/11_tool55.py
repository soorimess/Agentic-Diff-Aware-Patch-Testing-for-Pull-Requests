"""
Test for the Range(range(10)) behavior change.

This tests that Range no longer accepts range objects directly,
and instead raises a TypeError requiring explicit sympification.
"""

from sympy.sets.fancysets import Range
from sympy.core.sympify import sympify
from sympy import Symbol, S

def test_range_constructor_with_range_object():
    """Test that Range(range(10)) raises TypeError"""
    # This should raise TypeError now, not work as before
    try:
        r = Range(range(10))
        # If we get here, the old behavior still exists
        assert False, "Range(range(10)) should raise TypeError"
    except TypeError as e:
        # This is the expected new behavior - check the error message
        assert 'use sympify' in str(e)
    except Exception as e:
        # Any other exception is unexpected
        raise e

def test_range_constructor_with_sympified_range():
    """Test that sympify(range(10)) works correctly"""
    # This should work - explicit sympification
    r = sympify(range(10))
    # Should be a Range object
    assert isinstance(r, Range)
    # Should be equivalent to Range(10)
    assert r == Range(10)

def test_range_constructor_normal_behavior():
    """Test that normal Range construction still works"""
    # Test normal integer ranges
    r1 = Range(10)
    assert r1 == Range(0, 10, 1)
    
    r2 = Range(5, 15)
    assert r2 == Range(5, 15, 1)
    
    r3 = Range(0, 20, 2)
    assert r3 == Range(0, 20, 2)

def test_range_constructor_with_infinity():
    """Test that Range with infinity still works"""
    # Test infinite ranges
    r1 = Range(0, S.Infinity)
    assert isinstance(r1, Range)
    
    r2 = Range(S.NegativeInfinity, 10)
    assert isinstance(r2, Range)
    
    # Test with infinity and step
    r3 = Range(0, S.Infinity, 2)
    assert isinstance(r3, Range)

def test_range_constructor_invalid_arguments():
    """Test that invalid arguments still raise appropriate errors"""
    # Test non-integer arguments that should still fail
    try:
        # This should raise ValueError for non-integer arguments
        r = Range(1.5, 10, 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
    
    try:
        # This should raise ValueError for non-integer arguments  
        r = Range(0, 10.5, 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

def test_range_constructor_with_invalid_step():
    """Test that invalid step values still raise errors"""
    try:
        # This should raise ValueError for zero step
        r = Range(0, 10, 0)
        assert False, "Should have raised ValueError for zero step"
    except ValueError:
        pass  # Expected

def test_range_getitem_functionality():
    """Test Range __getitem__ functionality to exercise new validation logic"""
    # Test basic indexing
    r = Range(10)
    assert r[0] == 0
    assert r[5] == 5
    assert r[-1] == 9
    
    # Test with step
    r2 = Range(0, 10, 2)
    assert r2[0] == 0
    assert r2[1] == 2
    assert r2[-1] == 8
    
    # Test with symbolic ranges (if they work)
    n = Symbol('n', integer=True)
    try:
        r3 = Range(n, n + 10, 1)
        # This should work if symbolic ranges are supported
        if hasattr(r3, '__getitem__'):
            # Test indexing on symbolic range if possible
            pass
    except Exception:
        # Symbolic ranges might not work in old code but that's OK for this test
        pass