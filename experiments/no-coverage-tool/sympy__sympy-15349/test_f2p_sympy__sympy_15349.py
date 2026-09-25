"""
Test specifically for the quaternion rotation matrix bug fix.

The bug was in Quaternion.to_rotation_matrix() where m12 was calculated as:
2*s*(q.c*q.d + q.b*q.a) instead of 
2*s*(q.c*q.d - q.b*q.a)
"""

from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_rotation_matrix_m12_sign_correctness():
    """
    Test that verifies the m12 element of 2x2 rotation matrix is computed correctly.
    
    The bug: m12 element had wrong sign in calculation.
    Before fix: m12 = 2*s*(q.c*q.d + q.b*q.a)
    After fix:  m12 = 2*s*(q.c*q.d - q.b*q.a)
    
    For q = cos(x/2) + sin(x/2)*i + 0*j + 0*k:
    - Before fix: m12 = 2*1*(0 + sin(x/2)*cos(x/2)) = sin(x)
    - After fix:  m12 = 2*1*(0 - sin(x/2)*cos(x/2)) = -sin(x)
    
    This asserts that we see the correct sign is present.
    """
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get un-simplified matrix elements for direct comparison 
    matrix = q.to_rotation_matrix()
    
    # The critical m12 element - this is where we check the difference  
    m12_before_trig_simplification = matrix[1, 2]
    
    # This should be -sin(x) after fix (because we want m12 = -2*sin(x/2)*cos(x/2) = -sin(x))
    # Let's make it more indirect to focus on the actual changed feature
    
    # Before the fix (and with the numerical effect) m12 evaluated to sin(x) 
    # After the fix m12 should evaluate to -sin(x)
    # Let's use a better mathematical test:
    
    # The key insight from the error in rotation matrix is straightforward:
    # A rotation matrix around x-axis should have:
    # [[1, 0, 0], 
    #  [0, cos(x), -sin(x)],
    #  [0, sin(x), cos(x)]]
    
    # But due to the bug, it was giving:
    # [[1, 0, 0], 
    #  [0, cos(x), sin(x)],     # Incorrect sign here!
    #  [0, sin(x), cos(x)]]
    
    # So let's make this test check that m12 equals -sin(x) in the result
    simplified_matrix = trigsimp(matrix) 
    
    # After the fix, m12 should be -sin(x)  
    # If we don't apply the fix, m12 would be +sin(x)
    # I can't simply assert the expression equality, so I'll check:
    # For rotation around x-axis, sine terms should have the correct sign
    assert simplified_matrix[1, 2] == -sin(x), "m12 should be -sin(x) for correct x-axis rotation"
    
    # The matrix elements with the tricky signs should be correct  
    assert simplified_matrix[2, 1] == sin(x), "m21 should be sin(x) for correct rotation matrix"