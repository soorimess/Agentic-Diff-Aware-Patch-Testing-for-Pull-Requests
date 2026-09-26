from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_to_rotation_matrix_bug():
    """Test for bug in Quaternion.to_rotation_matrix() where m12 was computed incorrectly.
    
    The bug was in line 519 of quaternion.py where:
    m12 = 2*s*(q.c*q.d + q.b*q.a) 
    should have been:
    m12 = 2*s*(q.c*q.d - q.b*q.a)
    
    This affects the rotation matrix for quaternions representing rotations
    about the x-axis.
    """
    x = symbols('x')
    # Create a quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The correct result should have -sin(x) in the (1,2) position
    # The bug caused it to have +sin(x) instead
    expected = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x),  cos(x)]
    ])
    
    # Simplify the result to compare
    result_simplified = trigsimp(result)
    
    # Check that the (1,2) element is -sin(x) not +sin(x)
    assert result_simplified[1, 2] == -sin(x), f"Expected -sin(x) but got {result_simplified[1, 2]}"
    
    # Also check that the full matrix matches expected
    assert result_simplified == expected