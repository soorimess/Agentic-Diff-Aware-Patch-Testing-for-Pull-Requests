"""
Regression test for pull request that changes comparison behavior.

This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, allowing proper symmetric comparison
with custom classes.
"""

from sympy import Symbol, Integer
from sympy.core.basic import Basic
from sympy.core.sympify import SympifyError


def test_sympy_objects_return_not_implemented_on_sympify_error():
    """
    Test that SymPy objects return NotImplemented when __eq__ encounters 
    a type that cannot be sympified.
    """
    
    # Create a class that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Create a SymPy symbol
    x = Symbol('x')
    
    # Create a non-sympifiable object
    non_symp_obj = NonSympifiableClass()
    
    # Test that the __eq__ method returns NotImplemented instead of False
    # This is the core behavior change being tested
    result = x.__eq__(non_symp_obj)
    
    # Before the fix: result would be False
    # After the fix: result should be NotImplemented
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_integer_objects_return_not_implemented_on_sympify_error():
    """
    Test that Integer objects also return NotImplemented when __eq__ encounters 
    a type that cannot be sympified.
    """
    
    # Create a class that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Create an Integer
    i = Integer(5)
    
    # Create a non-sympifiable object
    non_symp_obj = NonSympifiableClass()
    
    # Test that the __eq__ method returns NotImplemented instead of False
    result = i.__eq__(non_symp_obj)
    
    # Before the fix: result would be False  
    # After the fix: result should be NotImplemented
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_comparison_delegation_works():
    """
    Test that the NotImplemented return enables proper comparison delegation.
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
    
    # Test that comparison works properly
    # When x.__eq__(custom_obj) is called, it should return NotImplemented
    # so that Python can try custom_obj.__eq__(x) instead
    
    result = x.__eq__(custom_obj)
    
    # The key is that it returns NotImplemented to enable delegation
    assert result is NotImplemented, f"Expected NotImplemented for delegation, got {result}"