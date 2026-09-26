"""
Regression test for Quaternion.to_rotation_matrix() bug.

This test ensures that the sign error in the to_rotation_matrix method
is caught. The bug was in line 532 of quaternion.py where the sign
of one term was incorrectly set.
"""

from sympy import symbols, trigsimp, cos, sin, Matrix
from sympy.algebras.quaternion import Quaternion


def test_quaternion_rotation_matrix_x_axis_sign():
    """Test that to_rotation_matrix produces correct signs for x-axis rotation."""
    # Create quaternion representing rotation around x-axis
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The correct result should have a negative sin(x) in the (1,2) position
    # and positive sin(x) in the (2,1) position for x-axis rotation
    expected = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]
    ])
    
    # Simplify the result to make comparison easier
    result_simplified = trigsimp(result)
    
    # Check that the result matches expected (the bug was in sign of sin(x))
    assert result_simplified == expected