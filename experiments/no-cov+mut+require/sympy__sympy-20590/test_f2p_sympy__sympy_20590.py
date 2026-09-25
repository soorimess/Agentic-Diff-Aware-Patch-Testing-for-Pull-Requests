"""
Test for Symbol __dict__ behavior regression.
"""
from sympy import Symbol


def test_symbol_has_dict():
    """Test that Symbol instances have __dict__ (the fix behavior)."""
    s = Symbol('s')
    # This should work after the fix was applied 
    # (the bug was that Symbol instances didn't have __dict__)
    dict_attr = s.__dict__ 
    assert isinstance(dict_attr, dict)
    assert dict_attr == {}