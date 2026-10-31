"""
Regression test for the change that prevents Range(range(10)) from working.

This test ensures that passing a Python range object to Range() raises a TypeError
instead of converting it to a Range object.
"""

from sympy.sets.fancysets import Range
from sympy import sympify
import sys

def test_range_constructor_with_python_range():
    """Test that Range(range(10)) raises TypeError"""
    # This should raise TypeError now
    try:
        result = Range(range(10))
        # If we get here, the test failed - it should have raised an error
        assert False, "Range(range(10)) should raise TypeError"
    except TypeError as e:
        assert 'use sympify' in str(e)
        assert 'to convert range to Range' in str(e)

def test_range_constructor_with_sympified_range():
    """Test that sympify(range(10)) works correctly"""
    # This should work - sympifying a range should convert it properly
    r = range(10)
    sympified = sympify(r)
    # The sympified object should be a Range
    assert sympified.__class__.__name__ == 'Range'
    # And it should be equivalent to Range(10)
    expected = Range(10)
    assert sympified == expected

def test_range_constructor_with_range_args():
    """Test that Range with explicit range arguments still works"""
    # These should still work - explicit integer arguments
    result1 = Range(10)
    result2 = Range(0, 10)
    result3 = Range(0, 10, 1)
    
    assert list(result1) == list(range(10))
    assert list(result2) == list(range(10))
    assert list(result3) == list(range(10))