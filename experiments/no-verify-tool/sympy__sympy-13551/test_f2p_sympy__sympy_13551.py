"""
Test for the product evaluation bug fix.

The bug was in how products of addition expressions were evaluated.
For Product(n + 1/2**k, [k, 0, n-1]), the wrong result was being returned
instead of the correct mathematical result.
"""

from sympy import Product
from sympy.abc import n, k


def test_product_addition_evaluation():
    """Test that Product(n + 1/2**k, [k, 0, n-1]) evaluates correctly."""
    # Create the problematic product
    p = Product(n + 1 / 2**k, [k, 0, n-1])
    
    # For n=2, the incorrect result was 9/2 due to wrong computation
    # The correct result should be 15/2: (2+1) * (2+1/2) = 3 * 2.5 = 15/2
    correct_result_n2 = 15/2
    actual_result_n2 = p.doit().subs(n, 2)
    
    # This assertion confirms the specific bug: wrong evaluation of sum of products instead of product of sums
    assert actual_result_n2 == correct_result_n2, (
        f"Product evaluation is incorrect. Expected {correct_result_n2}, "
        f"but got {actual_result_n2}. This indicates that products of addition terms "
        f"are incorrectly evaluated by summing the products of individual terms."
    )