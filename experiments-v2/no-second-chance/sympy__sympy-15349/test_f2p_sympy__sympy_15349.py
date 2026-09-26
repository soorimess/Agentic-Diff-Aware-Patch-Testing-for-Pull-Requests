"""Test for Quaternion.to_rotation_matrix() bug fix.

This test verifies the fix for the bug where Quaternion.to_rotation_matrix() 
was producing incorrect results due to a sign error in the m12 element.
"""

from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_to_rotation_matrix_bug():
    """Test that reproduces the bug in to_rotation_matrix() where m12 was wrong."""
    x = symbols('x')
    # Create a quaternion representing rotation around x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The correct result should have -sin(x) in the (1,2) position
    # The bug was that it had +sin(x) instead (which is 2*sin(x/2)*cos(x/2))
    # After applying trigsimp, the matrix should match:
    expected_correct = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    
    # Check that the matrix elements are correct after trigonometric simplification
    # Specifically, check the [1,2] element which was wrong
    assert trigsimp(result[1, 2]) == -sin(x)
    
    # Also check that [2,1] element is correct (should be sin(x), not -sin(x))
    assert trigsimp(result[2, 1]) == sin(x)
    
    # Verify that the full matrix matches when simplified
    # Check key elements that are mathematically significant
    assert trigsimp(result[0, 0]) == expected_correct[0, 0]
    assert trigsimp(result[1, 1]) == expected_correct[1, 1]
    assert trigsimp(result[2, 2]) == expected_correct[2, 2]
    
    # Additional verification: the determinant should be 1 for a rotation matrix
    # This is a good sanity check that our matrix is a proper rotation matrix
    det = result.det()
    assert trigsimp(det) == 1