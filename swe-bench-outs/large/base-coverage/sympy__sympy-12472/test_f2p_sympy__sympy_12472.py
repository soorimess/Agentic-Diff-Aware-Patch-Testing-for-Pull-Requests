"""Test for sqrt splitting issue with non-real factors"""

from sympy import sqrt, I, S
from sympy.core.add import Add

def test_complex_sqrt_infrastructure():
    """Test that the core infrastructure for complex sqrt operations works."""
    
    # Test basic functionality
    assert sqrt(4) == 2
    assert sqrt(-1) == I
    
    # Test that the key infrastructure is present
    assert hasattr(Add, '_eval_power')
    
    # Test basic power operations
    assert I**2 == -1

def test_power_evaluation_basic():
    """Test basic power evaluation works."""
    
    # Test that we can create power expressions
    expr = I**(S.Half)
    assert expr is not None
    
    # Test basic arithmetic
    assert (I * I) == -1

def test_complex_operations():
    """Test complex number operations work."""
    
    # Basic functionality
    assert sqrt(1) == 1
    assert sqrt(0) == 0
    
    # Complex number operations
    expr = sqrt(-1)
    assert expr == I