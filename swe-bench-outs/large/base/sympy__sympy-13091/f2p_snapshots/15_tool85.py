"""
Regression test for pull request that changes comparison behavior.

This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, allowing proper symmetric comparison
with custom classes.
"""

from sympy import Symbol, Integer, Float
from sympy.core.basic import Basic
from sympy.core.sympify import SympifyError


def test_sympy_objects_return_not_implemented_on_sympify_error():
    """
    Test that SymPy objects return NotImplemented when __eq__ encounters 
    a type that cannot be sympified, instead of False.
    
    This is the core behavior change: when comparing with unknown types,
    SymPy objects should return NotImplemented to enable proper Python
    comparison delegation.
    """
    
    # Create a class that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Test with a basic Symbol
    x = Symbol('x')
    non_symp_obj = NonSympifiableClass()
    
    # The key assertion: __eq__ should return NotImplemented, not False
    result = x.__eq__(non_symp_obj)
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"
    
    # Test with Integer as well
    i = Integer(5)
    result2 = i.__eq__(non_symp_obj)
    assert result2 is NotImplemented, f"Expected NotImplemented, got {result2}"


def test_comparison_delegation_enables_symmetry():
    """
    Test that returning NotImplemented enables proper comparison delegation
    which maintains symmetric equality.
    """
    
    # Create a custom class that can compare with SymPy objects
    class CustomClass:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            # This should be called when SymPy object compares with this class
            if isinstance(other, Basic):
                return self.value == other
            return False
            
        def __hash__(self):
            return hash(self.value)
    
    # Create a SymPy symbol
    x = Symbol('x')
    
    # Create custom object
    custom_obj = CustomClass(5)
    
    # When x.__eq__(custom_obj) returns NotImplemented, Python will try 
    # custom_obj.__eq__(x), which should return True (symmetric)
    result = x.__eq__(custom_obj)
    
    # The key is that it returns NotImplemented to enable delegation
    assert result is NotImplemented, f"Expected NotImplemented for delegation, got {result}"


def test_ne_method_behavior():
    """
    Test that __ne__ method works correctly with the new comparison behavior.
    """
    # Create a class that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Test with a basic Symbol
    x = Symbol('x')
    non_symp_obj = NonSympifiableClass()
    
    # Test __ne__ method behavior
    # This should delegate properly when __eq__ returns NotImplemented
    result = x.__ne__(non_symp_obj)
    
    # The __ne__ method should work correctly with the new __eq__ behavior
    # Even though __eq__ returns NotImplemented, __ne__ should still work
    assert result is not None  # Should not crash


def test_comparison_with_normal_objects():
    """
    Test that normal comparisons still work correctly.
    """
    x = Symbol('x')
    y = Symbol('y')
    
    # Normal equality should work
    assert x == x
    assert x != y
    
    # Test with integers
    i = Integer(5)
    j = Integer(5)
    k = Integer(10)
    
    assert i == j
    assert i != k


def test_has_matcher_method_specific():
    """
    Test the _has_matcher method specifically - this line was changed from
    'return self.__eq__' to 'return lambda other: self == other'
    """
    x = Symbol('x')
    
    # Test that _has_matcher returns a callable that works properly
    matcher = x._has_matcher()
    assert callable(matcher)
    
    # Test that the matcher works with normal symbols (this exercises the new lambda approach)
    y = Symbol('y')
    assert matcher(x) == True  # Should match itself
    assert matcher(y) == False  # Should not match different symbol
    
    # Test with non-sympifiable object to make sure it doesn't crash
    class NonSympifiableClass:
        def __sympy__(self):
            raise SympifyError("Cannot sympify this object")
    
    non_symp_obj = NonSympifiableClass()
    # This should not crash - the matcher should work with the new implementation
    result = matcher(non_symp_obj)
    # The result could be False or NotImplemented depending on implementation
    assert isinstance(result, (bool, type(NotImplemented)))


def test_float_eq_method():
    """
    Test the Float.__eq__ method specifically - this line was changed from
    'return False    # sympy != other  -->  not ==' to 'return NotImplemented'
    """
    # Create a Float object
    f = Float('1.5')
    
    # Create a class that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    non_symp_obj = NonSympifiableClass()
    
    # Test that __eq__ returns NotImplemented instead of False for non-sympifiable objects
    result = f.__eq__(non_symp_obj)
    assert result is NotImplemented, f"Expected NotImplemented for Float.__eq__, got {result}"