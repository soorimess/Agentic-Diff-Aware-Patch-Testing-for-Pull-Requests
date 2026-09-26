"""Test for quaternion to_rotation_matrix bug fix."""

from sympy import symbols, cos, sin, trigsimp
from sympy.algebras.quaternion import Quaternion


def test_quaternion_to_rotation_matrix_bug():
    """Test that to_rotation_matrix produces correct result for x-axis rotation.
    
    The bug was in line 528 of quaternion.py where m12 = 2*s*(q.c*q.d + q.b*q.a)
    should have been m12 = 2*s*(q.c*q.d - q.b*q.a). This caused incorrect signs
    in the rotation matrix for rotations about the x-axis.
    """
    x = symbols('x')
    # Create a quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The correct result should have sin(x) with negative sign in position (1,2)
    # Expected matrix:
    # [[1,      0,      0],
    #  [0, cos(x), -sin(x)],
    #  [0, sin(x),  cos(x)]]
    
    # Check that the matrix element at (1,2) equals -sin(x) after simplification
    # The buggy code produces 2*sin(x/2)*cos(x/2) which equals sin(x)
    # The correct code produces -2*sin(x/2)*cos(x/2) which equals -sin(x)
    simplified_m12 = trigsimp(matrix[1, 2])
    assert simplified_m12 == -sin(x), f"Position (1,2) should be -sin(x) but got {simplified_m12}"