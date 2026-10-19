"""
Test for the Range(range(10)) behavior change.

This tests that Range no longer accepts range objects directly,
and instead raises a TypeError requiring explicit sympification.
"""

from sympy.sets.fancysets import Range
from sympy.core.sympify import sympify

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