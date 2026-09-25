"""
Regression test for Quaternion.to_rotation_matrix() bug fix.
This tests the specific case mentioned in the bug report.
"""

from sympy import symbols, cos, sin, trigsimp
from sympy.algebras.quaternion import Quaternion


def test_quaternion_rotation_matrix_sign_bug():
    """
    Test for the specific case reported in the bug where 
    Quaternion.to_rotation_matrix() had incorrect signs.
    
    The bug was in the m12 element of the rotation matrix.
    For q = Quaternion(cos(x/2), sin(x/2), 0, 0), 
    the result should have -sin(x) in position (1,2), not sin(x).
    """
    x = symbols('x')
    # Create quaternion as described in bug report
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get rotation matrix and simplify
    matrix = q.to_rotation_matrix()
    simplified = trigsimp(matrix)
    
    # The bug was that element (1,2) was sin(x) instead of -sin(x)
    # This assertion should pass after the fix, fail before the fix
    assert simplified[1, 2] == -sin(x), f"Element (1,2) should be -sin(x) but is {simplified[1, 2]}"