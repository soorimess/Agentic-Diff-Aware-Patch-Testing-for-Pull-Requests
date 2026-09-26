"""
Test for Quaternion.to_rotation_matrix() bug fix.

This test verifies that the to_rotation_matrix method produces the correct
rotation matrix by checking the specific matrix element that was fixed in the diff.
"""

from sympy import symbols, trigsimp, cos, sin
from sympy.algebras.quaternion import Quaternion


def test_matrix_element_m12_fix():
    """Test that element [1,2] is -sin(x) after the fix is applied."""
    x = symbols('x')
    # Create quaternion representing rotation about x-axis by angle x
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The diff changed m12 from 2*s*(q.c*q.d + q.b*q.a) to 2*s*(q.c*q.d - q.b*q.a)
    # For our case: q.c=0, q.d=0, q.b=sin(x/2), q.a=cos(x/2)
    # So m12 = 2*s*(0*0 - sin(x/2)*cos(x/2)) = -2*sin(x/2)*cos(x/2) = -sin(x) 
    # Element [1,2] should be -sin(x) with the fix applied
    assert trigsimp(result[1, 2]) == -sin(x)