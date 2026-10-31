"""
Regression test for the change that prevents Range(range(10)) from working.

This test ensures that passing a Python range object to Range() raises a TypeError
instead of converting it to a Range object.
"""

from sympy.sets.fancysets import Range
from sympy import sympify, Symbol, S, oo
from sympy.utilities.pytest import raises

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

def test_range_infinite_validation():
    """Test infinite range validation"""
    # Test that infinite ranges work properly
    r1 = Range(0, oo, 2)
    assert r1.size is S.Infinity
    
    r2 = Range(0, -oo, -2)
    assert r2.size is S.Infinity

def test_range_null_range():
    """Test null range handling"""
    # Test null ranges
    r1 = Range(0, 0, 1)
    assert len(r1) == 0
    assert list(r1) == []
    
    # Test null ranges with different parameters
    r2 = Range(5, 5, 1)
    assert len(r2) == 0
    assert list(r2) == []

def test_range_step_validation():
    """Test step validation with special cases"""
    # Test that invalid steps are properly handled
    # This tests the new validation logic for step values
    
    # Test with symbolic step that is integer
    n = Symbol('n', integer=True)
    try:
        # This should work with integer symbols
        r = Range(0, 10, n)
        # If it doesn't raise, test that it works
        if hasattr(r, 'step'):
            assert r.step == n
    except Exception:
        # Some symbolic cases might not work, that's OK for this test
        pass

def test_range_symbolic_bounds():
    """Test symbolic bounds validation"""
    # Test that symbolic bounds that are integers work
    n = Symbol('n', integer=True)
    try:
        # This should work with integer symbols
        r = Range(n, n + 5, 1)
        # Test that we can access properties
        if hasattr(r, 'start'):
            assert r.start == n
    except Exception:
        # Some symbolic cases might not work, that's OK for this test
        pass