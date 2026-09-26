from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin

def test_quaternion_to_rotation_matrix_x_axis_sign():
    """
    Regression test for Quaternion.to_rotation_matrix() bug where the sign
    of the (2,1) element was incorrect for x-axis rotations.
    
    The bug was in line 532 of quaternion.py where:
    m12 = 2*s*(q.c*q.d + q.b*q.a) 
    should have been:
    m12 = 2*s*(q.c*q.d - q.b*q.a)
    
    For a quaternion representing rotation around the x-axis:
    q = cos(x/2) + sin(x/2)*i + 0*j + 0*k
    
    The correct rotation matrix should have:
    matrix[2,1] = -sin(x)  # This is the bug - it was returning sin(x)
    
    This test ensures that the (2,1) element of the rotation matrix
    correctly represents -sin(x) rather than sin(x).
    """
    x = symbols('x')
    
    # Create a quaternion representing rotation around x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The (2,1) element should be -sin(x) for a proper x-axis rotation matrix
    actual_m21 = matrix[2, 1]
    expected_m21 = -sin(x)
    
    # This assertion will fail with the buggy code and pass with the fixed code
    assert trigsimp(actual_m21) == trigsimp(expected_m21)