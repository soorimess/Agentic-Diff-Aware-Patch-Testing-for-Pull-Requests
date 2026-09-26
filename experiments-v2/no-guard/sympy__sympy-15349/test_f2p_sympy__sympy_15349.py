"""Test for Quaternion.to_rotation_matrix() bug fix."""

from sympy import symbols, cos, sin, trigsimp, Matrix
from sympy.algebras.quaternion import Quaternion


def test_quaternion_rotation_matrix_sign_bug():
    """Test that to_rotation_matrix produces correct signs in rotation matrix."""
    # This test reproduces the bug described in the issue
    # The bug is in the m12 element of the rotation matrix
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The bug causes m12 to be positive sin(x) instead of negative
    # Check that m12 is indeed -sin(x) (not sin(x))
    m12 = result[1, 2]
    
    # The correct result should be -sin(x) 
    # But due to the bug it's currently sin(x)
    expected_m12 = -sin(x)
    
    # Check that we get the correct sign
    assert trigsimp(m12) == expected_m12, f"Expected m12 to be {expected_m12}, but got {trigsimp(m12)}"
    
    # Also verify the full matrix is correct
    expected_matrix = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]
    ])
    
    simplified_result = trigsimp(result)
    assert simplified_result == expected_matrix, f"Expected matrix {expected_matrix}, but got {simplified_result}"