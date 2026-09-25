"""Test for the Quaternion.to_rotation_matrix() bug.

This test specifically checks for a bug in the m12 element
of the rotation matrix calculation where it was computing
2*s*(q.c*q.d + q.b*q.a) instead of 2*s*(q.c*q.d - q.b*q.a).

The bug would cause the wrong sign in the rotation matrix for
quaternions representing rotation about x-axis.
"""

from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_rotation_matrix_m12_sign():
    """Test that the m12 element in rotation matrix has correct sign."""
    x = symbols('x')
    
    # Create a quaternion representing rotation around x-axis  
    # q = Quaternion(cos(x/2), sin(x/2), 0, 0) 
    # This should produce a rotation matrix with -sin(x) in position (1,2)
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    rotation_matrix = q.to_rotation_matrix()
    simplified_matrix = trigsimp(rotation_matrix)
    
    # The fixed version should have -sin(x) in position [1,2] for x-axis rotation
    # The buggy version erroneously had sin(x) in this position
    assert simplified_matrix[1, 2] == -sin(x), f"Expected -sin(x) but got {simplified_matrix[1, 2]}"