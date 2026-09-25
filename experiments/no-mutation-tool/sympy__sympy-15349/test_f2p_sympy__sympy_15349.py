"""
Test for the quaternion rotation matrix bug.
This test captures the bug where to_rotation_matrix()
produced incorrect results for specific quaternion inputs.
"""

from sympy import symbols, cos, sin, trigsimp
from sympy.algebras.quaternion import Quaternion


def test_quaternion_rotation_matrix_sign_error():
    """
    Test that detects the sign error in the (1,2) element of the quaternion 
    rotation matrix that was specifically identified in the bug report.
    
    For a quaternion q = [cos(x/2), sin(x/2), 0, 0] representing 
    rotation about x-axis, the to_rotation_matrix() method should produce:
    
    Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],  # <-- correct (1,2) element should be -sin(x)  
        [0, sin(x), cos(x)]    # <-- correct (2,1) element should be sin(x)
    ])
    
    But the bug incorrectly computed it as:
    
    Matrix([
        [1,      0,      0],
        [0, cos(x),  sin(x)],  # <-- bug: should be -sin(x)
        [0, sin(x), cos(x)]    # <-- this was correct
    ])
    
    The bug was in the line m12 = 2*s*(q.c*q.d + q.b*q.a) which should be
    m12 = 2*s*(q.c*q.d - q.b*q.a) 
    """
    x = symbols('x')
    
    # Create a quaternion representing rotation about x-axis  
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The matrix should be properly simplified using trigsimp
    matrix_simplified = [[trigsimp(matrix[i,j]) for j in range(3)] for i in range(3)]
    
    # Check the specific bug: (1,2) element should be -sin(x), not sin(x)
    # This checks that the fix to line 532 is working correctly
    m12_value = matrix_simplified[1][2]
    m21_value = matrix_simplified[2][1] 
    
    # Even with trigsimp, the correct values should be:
    # m12 = -sin(x)
    # m21 = sin(x)
    assert m12_value == -sin(x), f"Bug: m12 is {m12_value}, expected -sin(x)"
    assert m21_value == sin(x), f"Bug: m21 is {m21_value}, expected sin(x)"