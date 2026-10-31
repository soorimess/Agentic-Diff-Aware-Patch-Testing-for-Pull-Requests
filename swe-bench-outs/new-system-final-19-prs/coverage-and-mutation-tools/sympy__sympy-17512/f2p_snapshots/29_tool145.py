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

def test_range_symbolic_basic():
    """Test basic symbolic range functionality"""
    # Test symbolic ranges that should work
    n = Symbol('n', integer=True)
    r = Range(n, n + 20, 3)
    
    # These should work without error
    assert r.start == n
    assert r.step == 3
    assert r.inf == n  # This should work for integer symbols

def test_range_symbolic_size():
    """Test symbolic range size calculation"""
    n = Symbol('n', integer=True)
    r = Range(n, n + 10, 1)
    
    # Test that size works for symbolic ranges (should be 10)
    size = r.size
    assert size == 10

def test_range_symbolic_getitem():
    """Test symbolic range indexing"""
    n = Symbol('n', integer=True)
    r = Range(n, n + 5, 1)
    
    # Test accessing elements from symbolic ranges
    first = r[0]  # Should work
    assert first == n
    
    last = r[-1]  # Should work
    assert last == n + 4

def test_range_symbolic_inf_sup():
    """Test symbolic range inf and sup"""
    n = Symbol('n', integer=True)
    r = Range(n, n + 10, 1)
    
    # Test inf and sup
    inf_val = r.inf
    sup_val = r.sup
    # These should not raise errors
    assert inf_val == n
    assert sup_val == n + 9

def test_range_getitem_normal():
    """Test normal __getitem__ functionality"""
    # Test normal range indexing
    r = Range(10)
    assert r[0] == 0
    assert r[-1] == 9
    assert r[-2] == 8