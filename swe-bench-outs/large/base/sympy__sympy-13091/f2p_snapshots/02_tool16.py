"""
Regression test for pull request that changes comparison behavior.

This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, allowing proper symmetric comparison
with custom classes.
"""

from sympy import Symbol, Integer
from sympy.core.basic import Basic
from sympy.core.sympify import SympifyError


def test_basic_comparison_returns_not_implemented():
    """Test that basic SymPy objects return NotImplemented for unknown types."""
    
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
    
    # Test that the __eq__ method returns NotImplemented when comparing
    # with an object that can't be sympified
    # This is the core behavior change we're testing
    
    # We'll test by creating an object that raises SympifyError when sympified
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Create a non-sympifiable object
    non_symp_obj = NonSympifiableClass()
    
    # Test the __eq__ method directly
    result = x.__eq__(non_symp_obj)
    
    # This is the key assertion: the result should be NotImplemented
    # This allows Python to delegate to the other object's __eq__ method
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_integer_comparison_returns_not_implemented():
    """Test that Integer objects return NotImplemented for unknown types."""
    
    # Create a non-sympifiable object
    class NonSympifiableClass:
        def __sympy__(self):
            # This will raise an error to make it non-sympifiable
            raise SympifyError("Cannot sympify this object")
    
    # Create an Integer
    i = Integer(5)
    
    # Create a non-sympifiable object
    non_symp_obj = NonSympifiableClass()
    
    # Test the __eq__ method directly
    result = i.__eq__(non_symp_obj)
    
    # This should also return NotImplemented
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_comparison_symmetry():
    """Test that comparison is symmetric with custom classes."""
    
    # Create a custom class that implements __eq__ to work with SymPy objects
    class Foo:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            # This should be called when SymPy object compares with this class
            if isinstance(other, Symbol):
                return self.value == other
            return False
    
    # Create a SymPy symbol
    s = Symbol('s')
    
    # Create custom object
    f = Foo(5)
    
    # Test that both directions work properly
    # This tests the symmetric behavior that the change enables
    
    # The key is that when s.__eq__(f) is called, it should return NotImplemented
    # so that Python tries f.__eq__(s) instead of stopping at False
    result1 = s.__eq__(f)
    result2 = f.__eq__(s)
    
    # Both should be consistent - either both return True or both return False
    # But more importantly, s.__eq__(f) should return NotImplemented to allow delegation
    assert result1 is NotImplemented, f"Expected NotImplemented from s.__eq__(f), got {result1}"