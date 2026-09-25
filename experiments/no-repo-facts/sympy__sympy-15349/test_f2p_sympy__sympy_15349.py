"""
Regression test for quaternion.to_rotation_matrix() bug.

This test specifically verifies the fix for the bug where 
Quaternion.to_rotation_matrix() was producing incorrect signs.
"""

from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_rotation_matrix_sign_bug():
    """
    Test that to_rotation_matrix produces the correct sign for m12 element.
    
    The bug was in line 532 of quaternion.py where:
    m12 = 2*s*(q.c*q.d + q.b*q.a) 
    was incorrect and should be:
    m12 = 2*s*(q.c*q.d - q.b*q.a)
    
    For the specific case q = Quaternion(cos(x/2), sin(x/2), 0, 0),
    this should result in a rotation matrix about the x-axis,
    but with the wrong sign on element [1,2].
    """
    
    x = symbols('x')
    # Create quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # Simplify using trig identities
    simplified = trigsimp(matrix)
    
    # Test specific element that was affected by the bug  
    assert simplified[1, 2] == -sin(x), f"Element [1,2] should be -sin(x) but is {simplified[1, 2]}"