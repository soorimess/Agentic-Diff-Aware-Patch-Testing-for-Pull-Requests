"""
Regression test for the change that prevents Range(range(10)) from working.

This test ensures that passing a Python range object to Range() raises a TypeError
instead of converting it to a Range object.
"""

from sympy.sets.fancysets import Range
from sympy import sympify, Symbol, S, oo
from sympy.utilities.pytest import raises
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

def test_range_getitem_normal():
    """Test normal __getitem__ functionality"""
    # Test normal range indexing
    r = Range(10)
    assert r[0] == 0
    assert r[-1] == 9
    assert r[-2] == 8
    
    # Test slice operations
    r2 = Range(10)
    sliced = r2[2:5]
    assert isinstance(sliced, Range)
    assert list(sliced) == [2, 3, 4]

def test_range_contains():
    """Test _contains method functionality"""
    # Test that Range properly handles containment checks
    r = Range(10)
    
    # Test that integers in range are contained
    assert 5 in r
    assert 0 in r
    assert 9 in r
    
    # Test that integers outside range are not contained
    assert 10 not in r
    assert -1 not in r
    
    # Test with negative ranges
    r2 = Range(-5, 5)
    assert 0 in r2
    assert -5 in r2
    assert 4 in r2
    assert 5 not in r2
    assert -6 not in r2
    
    # Test with step parameter
    r3 = Range(0, 10, 2)
    assert 0 in r3
    assert 2 in r3
    assert 8 in r3
    assert 1 not in r3  # odd numbers not in even range
    assert 10 not in r3  # 10 is not in range (stops before 10)

def test_range_infinite_validation():
    """Test infinite range validation"""
    # Test that infinite ranges work properly
    r1 = Range(0, oo, 2)
    assert r1.size is S.Infinity
    
    r2 = Range(0, -oo, -2)
    assert r2.size is S.Infinity

def test_range_properties():
    """Test range properties and methods"""
    # Test basic range properties
    r = Range(5, 15, 2)
    assert r.start == 5
    assert r.stop == 15
    assert r.step == 2
    
    # Test inf and sup
    assert r.inf == 5
    assert r.sup == 13  # 5 + 2*4 = 13 (since 4 elements: 5,7,9,11,13)
    
    # Test length
    assert len(r) == 5
    
    # Test size property
    assert r.size == 5

def test_range_getitem_edge_cases():
    """Test edge cases in __getitem__ validation"""
    # Test with various range configurations that might trigger validation
    r1 = Range(100, 0, -10)  # Reverse range
    assert r1[0] == 100
    assert r1[-1] == 10
    
    r2 = Range(0, 100, 5)  # Forward range
    assert r2[0] == 0
    assert r2[-1] == 95
    
    # Test that we can get the first and last elements
    r3 = Range(20)
    assert r3[0] == 0
    assert r3[-1] == 19