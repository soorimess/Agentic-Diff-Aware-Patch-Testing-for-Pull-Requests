"""
Test for the rich comparison protocol fix.
This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, which allows proper symmetric comparison.
"""

from sympy import Symbol
from sympy.core.sympify import SympifyError


class CustomClass:
    """A custom class that implements __eq__ to compare with SymPy objects."""
    
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        # This should be called when comparing with SymPy objects
        if hasattr(other, '__class__') and 'Basic' in [cls.__name__ for cls in other.__class__.__mro__]:
            # If other is a SymPy Basic object, compare based on value
            return self.value == getattr(other, 'name', str(other))
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)


def test_comparison_symmetry():
    """Test that comparison is symmetric when custom objects are involved."""
    # Create a SymPy symbol
    x = Symbol('x')
    
    # Create a custom object
    custom_obj = CustomClass('x')
    
    # Test that the comparison works both ways
    # Before the fix: x == custom_obj would return False (because Basic.__eq__ returns False)
    # After the fix: x == custom_obj should delegate to custom_obj.__eq__ and return True
    
    # The key test is to check what happens when we compare with an unknown type
    # This should return NotImplemented to allow proper delegation
    
    # Test the specific behavior that changed
    result1 = x.__eq__(custom_obj)
    result2 = custom_obj.__eq__(x)
    
    # Both should return the same result (either True or NotImplemented)
    # But the key change is that x.__eq__(custom_obj) should return NotImplemented
    # instead of False, so that the comparison can be delegated properly
    
    # Let's test what happens with a known type that can't be sympified
    class UnknownType:
        pass
    
    unknown_obj = UnknownType()
    
    # This should return NotImplemented to allow proper delegation
    result3 = x.__eq__(unknown_obj)
    
    # Test that the behavior is now correct
    # When we compare with something that can't be sympified, 
    # we should return NotImplemented, not False
    assert result3 is NotImplemented, "SymPy objects should return NotImplemented for unknown types, not False"


def test_comparison_with_sympify_error():
    """Test that comparison with objects that cause SympifyError returns NotImplemented."""
    x = Symbol('x')
    
    # Create an object that will cause SympifyError when passed to _sympify
    class NonSympifiable:
        def __str__(self):
            return "non_sympifiable"
        
        def __sympy__(self):
            raise SympifyError("Cannot sympify this object")
    
    non_sympifiable_obj = NonSympifiable()
    
    # This should return NotImplemented, not False
    result = x.__eq__(non_sympifiable_obj)
    
    # The fix ensures this returns NotImplemented so Python can try the reverse comparison
    assert result is NotImplemented, "Should return NotImplemented for SympifyError cases"


def test_comparison_delegation():
    """Test that comparison properly delegates when NotImplemented is returned."""
    x = Symbol('x')
    
    class CustomEqClass:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            # Custom comparison logic
            if hasattr(other, 'name') and other.name == 'x':
                return True
            return False
    
    custom_obj = CustomEqClass('x')
    
    # Test that the comparison works properly
    # Before fix: x == custom_obj would be False (because Basic.__eq__ returns False)
    # After fix: x == custom_obj should delegate to custom_obj.__eq__ and return True
    
    # The key test is that when SymPy objects return NotImplemented, 
    # the comparison can be properly delegated
    result = x.__eq__(custom_obj)
    
    # This should be NotImplemented to allow proper delegation
    assert result is NotImplemented, "SymPy objects should return NotImplemented for unknown types"
    
    # Test the reverse comparison
    result_reverse = custom_obj.__eq__(x)
    # This should be True based on our custom implementation
    assert result_reverse is True, "Custom class should properly compare with SymPy objects"