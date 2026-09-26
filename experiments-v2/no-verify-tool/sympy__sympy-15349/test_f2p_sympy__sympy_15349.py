"""Test for Quaternion.to_rotation_matrix() bug fix.

This test verifies that the to_rotation_matrix method returns the correct
rotation matrix for quaternions, specifically checking that the (1,2) element
is computed correctly.
"""

from sympy import symbols, cos, sin, trigsimp
from sympy.algebras.quaternion import Quaternion


def test_quaternion_rotation_matrix_bug():
    """Test that demonstrates the bug in to_rotation_matrix() method.
    
    The bug was in the computation of m12 element of the rotation matrix.
    It should be 2*s*(q.c*q.d - q.b*q.a) but was incorrectly 2*s*(q.c*q.d + q.b*q.a)
    
    For a quaternion representing rotation about x-axis: q = [cos(x/2), sin(x/2), 0, 0]
    The correct (1,2) element should be -sin(x) but with the bug it was +sin(x)
    """
    x = symbols('x')
    
    # Create a quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The (1,2) element should be -sin(x) due to the bug it's currently +sin(x)
    actual_m12 = matrix[1, 2]
    
    # With the bug, we get sin(x) instead of -sin(x)
    # This is the key assertion that catches the bug
    assert trigsimp(actual_m12) == -sin(x), f"Bug present: Expected -sin(x) but got {trigsimp(actual_m12)}"


def test_quaternion_rotation_matrix_y_axis():
    """Test rotation about y-axis to verify the fix works generally."""
    x = symbols('x')
    
    # Create a quaternion representing rotation about y-axis
    q = Quaternion(cos(x/2), 0, sin(x/2), 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # For y-axis rotation, the (0,2) element should be sin(x) and (2,0) element should be -sin(x)
    actual_m02 = matrix[0, 2]
    actual_m20 = matrix[2, 0]
    
    # These should be correct (no bug in these elements)
    assert trigsimp(actual_m02) == sin(x), f"Expected sin(x) but got {trigsimp(actual_m02)}"
    assert trigsimp(actual_m20) == -sin(x), f"Expected -sin(x) but got {trigsimp(actual_m20)}"