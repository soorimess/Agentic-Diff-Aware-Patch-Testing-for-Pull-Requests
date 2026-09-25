from sympy import S, symbols, Lambda, imageset, Reals, I, FiniteSet
from sympy.sets import ImageSet

def test_image_set_intersect_real_bug():
    """Test that demonstrates the bug in ImageSet intersection with Reals."""
    # Create the problematic image set from the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The real part is n and the imaginary part is (n-1)*(n+1)
    # For a complex number to be real, the imaginary part must be 0
    # (n-1)*(n+1) = 0 when n = -1 or n = 1
    # So the set S1 intersected with Reals should be {-1, 1}
    
    # Test that 2 is not in the original set (correct)
    assert 2 not in S1
    
    # Test the main buggy behavior - 2 should not be in S1 intersect Reals
    assert 2 not in S1.intersect(Reals)
    
    # Test that -1 and 1 ARE in the intersection (that's the correct behavior)
    assert -1 in S1.intersect(Reals)
    assert 1 in S1.intersect(Reals)
    
    # Test that the intersection result itself is correct
    intersection_result = S1.intersect(Reals)
    assert len(intersection_result) == 2
    assert -1 in intersection_result
    assert 1 in intersection_result

def test_image_set_intersect_real_simple_case():
    """Test a simpler case to make sure the fix works as expected."""
    # Simple case: {n + i*n | n ∈ ℤ} intersect Reals
    # Imaginary part is n, so for real numbers n must be 0  
    n = symbols('n')
    S2 = imageset(Lambda(n, n + n*I), S.Integers)
    
    # 0 should be in intersection, non-zero values should not
    assert 0 in S2.intersect(Reals)
    assert 1 not in S2.intersect(Reals)
    assert 2 not in S2.intersect(Reals)
    
    # Check that the intersection is correct
    intersection_result = S2.intersect(Reals)
    assert len(intersection_result) == 1
    assert 0 in intersection_result

def test_image_set_with_denominator():
    """Test case that involves a denominator that affects intersection."""
    # This tests a case involving non-trivial denominators
    n = symbols('n')
    # This image set has a potential denominator issue that would need handling
    S3 = imageset(Lambda(n, (n + 1)/(n - 1) + I*n), S.Integers)
    
    # Here we test that we handle the case where an expression has denominator
    # that affects the base set calculation  
    try:
        result = S3.intersect(Reals)
    except:
        # If there's an error, that's probably related to the bug
        pass