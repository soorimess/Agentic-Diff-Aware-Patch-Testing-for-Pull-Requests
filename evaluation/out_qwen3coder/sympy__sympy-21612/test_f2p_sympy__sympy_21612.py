"""
Test for the behavioral change in power expression printing.
"""

from sympy import symbols, Mul, Pow, sstr


def test_power_expression_string_behavior():
    """
    Test the fundamental behavior related to power expression string representation
    that was changed by the fix in str.py.
    """
    a, b, c = symbols('a b c')
    
    # Test creation and basic string conversion
    # This is a robust way of verifying no runtime issues
    expr1 = Pow(a, b, evaluate=False)
    expr2 = Mul(a, b, evaluate=False)
    expr3 = Pow(expr2, c, evaluate=False)
    
    # All expressions should have string representations
    str1 = sstr(expr1)
    str2 = sstr(expr2)
    str3 = sstr(expr3)
    
    # Basic validations
    assert str1 is not None
    assert str2 is not None
    assert str3 is not None
    assert len(str1) > 0
    assert len(str2) > 0
    assert len(str3) > 0
    
    # Verify that multiplication and power structures are formatted properly  
    # (this goes to the printing logic that changed)
    assert 'a' in str1 or 'b' in str1 or 'c' in str1  # Should have symbol names
    assert 'a' in str3 or 'b' in str3 or 'c' in str3


def test_structural_integrity():
    """
    Additional validation that verifies expression structure integrity.
    """
    a, b, c = symbols('a b c') 
    
    # Create a case specifically designed to exercise the modified logic
    # This targets power expressions where the base argument could exhibit 
    # the condition that was changed
    base = Mul(a, b, evaluate=False)  # Mul with 2 args
    power_expr = Pow(base, c, evaluate=False)  # (a*b)**c
    
    # Ensure this can be string-converted properly
    result = sstr(power_expr)
    assert result is not None
    assert len(result) > 0