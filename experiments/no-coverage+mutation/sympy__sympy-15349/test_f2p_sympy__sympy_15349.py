"""
Test for Quaternion.to_rotation_matrix() bug fix

The bug was in the sign of one element in the rotation matrix calculation.
The fix changes the formula for m12 from:
    m12 = 2*s*(q.c*q.d + q.b*q.a)
to:
    m12 = 2*s*(q.c*q.d - q.b*q.a)
"""

from sympy import symbols, cos, sin, trigsimp, Matrix
from sympy.algebras.quaternion import Quaternion

def test_quaternion_rotation_matrix_sign():
    """Test that to_rotation_matrix produces the correct sign in m12 element."""
    x = symbols('x')
    
    # Create a quaternion representing rotation around x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The expected matrix should have negative sin(x) in the (2,1) position
    # This is the corrected version per the bug report
    result_simplified = trigsimp(result)
    
    # Verify that the m12 element (position [1,2]) is -sin(x) not sin(x)
    # This is the exact bug that was fixed
    assert result_simplified[1, 2] == -sin(x), \
        f"Bug present: m12 element should be -sin(x) but is {result_simplified[1, 2]}"

def test_quaternion_rotation_matrix_specific_elements():
    """Test that we get the expected structure with correct signs."""
    x = symbols('x')
    
    # Create quaternion for x-axis rotation
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    result = q.to_rotation_matrix()
    result_simplified = trigsimp(result)
    
    # Test key elements: 
    # The corrected matrix should be:
    # [[1, 0, 0], 
    #  [0, cos(x), -sin(x)], 
    #  [0, sin(x), cos(x)]]
    
    # Check the specific elements that were affected by the fix
    assert result_simplified[0, 0] == 1
    assert result_simplified[0, 1] == 0
    assert result_simplified[0, 2] == 0
    assert result_simplified[1, 0] == 0
    assert result_simplified[1, 1] == cos(x)
    assert result_simplified[1, 2] == -sin(x)  # This is the key element that was wrong
    assert result_simplified[2, 0] == 0
    assert result_simplified[2, 1] == sin(x)
    assert result_simplified[2, 2] == cos(x)