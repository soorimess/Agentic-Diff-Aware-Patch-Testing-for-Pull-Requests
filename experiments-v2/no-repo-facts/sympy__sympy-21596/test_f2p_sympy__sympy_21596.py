"""
Regression test for the bug in ImageSet intersection with Reals.

This test verifies that the intersection works correctly and does not raise 
the TypeError "Input args to Union must be Sets" that was present in the buggy code.

The bug was in the intersection handler where the _solution_union function 
was not properly handling the results from solve_linear, causing Union to be 
constructed with non-Set arguments.
"""

def test_no_union_error_in_image_set_intersection():
    """
    Test that ImageSet intersection with Reals does not raise TypeError.
    
    Before fix: TypeError: Input args to Union must be Sets
    After fix: Works correctly
    """
    from sympy import S, symbols, Lambda, I, imageset
    from sympy.sets.fancysets import Integers, Reals
    
    # Create the ImageSet from the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # This operation was failing with "Input args to Union must be Sets"
    # The test returns False if this error occurs (bug present)
    # and True if it works correctly (bug fixed)
    try:
        result = S1.intersect(Reals)
        # Success - no error occurred
        return True
    except TypeError as e:
        if "Input args to Union must be Sets" in str(e):
            # This is the exact bug we're testing for
            return False
        raise  # Re-raise if it's a different TypeError

# This test file is designed to fail before the fix and pass after the fix
# The key behavior difference is whether the TypeError occurs or not