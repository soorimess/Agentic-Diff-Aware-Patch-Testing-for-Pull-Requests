from sympy import *
from sympy.abc import n, k

def test_product_correctness():
    """Test that Product(n + 1/2**k, [k, 0, n-1]) gives correct result."""
    p = Product(n + 1 / 2**k, [k, 0, n-1])
    result = p.doit().subs(n, 2)
    # For n=2: (2+1)*(2+1/2) = 3*5/2 = 15/2
    assert result == Rational(15, 2)

if __name__ == "__main__":
    test_product_correctness()
    print("Test passed!")