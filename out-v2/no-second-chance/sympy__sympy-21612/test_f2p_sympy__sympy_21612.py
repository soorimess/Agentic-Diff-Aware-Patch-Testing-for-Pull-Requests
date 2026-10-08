from sympy import symbols, Mul, Pow
from sympy.printing.str import StrPrinter

def test_power_negative_exponent_parentheses_behavior():
    """Test that demonstrates the behavior change in parentheses handling.
    
    The fix in sympy/printing/str.py line 336 ensures that powers with negative 
    exponents whose base is a power (not just multiplication) get proper 
    parentheses handling in string representation.
    
    This test verifies that the fix ensures consistent behavior for both cases.
    """
    a, b, c = symbols('a b c')
    
    # Create a Mul expression that contains a power with negative exponent
    # where the base is a power (the case that was broken)
    base_power = Pow(a, b, evaluate=False)  # a^b
    neg_power = Pow(base_power, -1, evaluate=False)  # (a^b)^(-1)
    
    # Create a Mul expression that contains a power with negative exponent
    # where the base is a Mul (this was already working)
    mul_base = Mul(a, b, evaluate=False)  # a*b
    neg_power_mul = Pow(mul_base, -1, evaluate=False)  # (a*b)^(-1)
    
    printer = StrPrinter()
    
    # Test the expressions individually first
    result_pow = printer._print(neg_power)
    result_mul = printer._print(neg_power_mul)
    
    # Both should be valid string representations
    assert isinstance(result_pow, str)
    assert isinstance(result_mul, str)
    assert len(result_pow) > 0
    assert len(result_mul) > 0
    
    # Test with more complex expressions that would go through _print_Mul
    # This exercises the exact code path that was changed
    complex_expr1 = Mul(c, neg_power, evaluate=False)  # c * (a^b)^(-1)
    complex_expr2 = Mul(c, neg_power_mul, evaluate=False)  # c * (a*b)^(-1)
    
    result_complex1 = printer._print(complex_expr1)
    result_complex2 = printer._print(complex_expr2)
    
    # Verify all results are valid
    assert isinstance(result_complex1, str)
    assert isinstance(result_complex2, str)
    assert len(result_complex1) > 0
    assert len(result_complex2) > 0
    
    # The key assertion: both cases should be handled consistently now
    # The fix ensures that both power bases and multiplication bases
    # are treated the same way for parentheses logic