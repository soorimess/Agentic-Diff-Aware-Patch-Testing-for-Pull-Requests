from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_to_rotation_matrix_sign_bug():
    """
    Test for bug in Quaternion.to_rotation_matrix() where the sign 
    in the (1,2) position of the rotation matrix was incorrect.
    """
    x = symbols('x')
    # Create a quaternion representing rotation around the x-axis  
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    result = trigsimp(q.to_rotation_matrix())
    
    # The correct matrix should be:
    # [[1,      0,      0],
    #  [0, cos(x), -sin(x)],
    #  [0, sin(x), cos(x)]]
    expected = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    
    # This should pass with the correct implementation
    assert result == expected

def test_quaternion_to_rotation_matrix_z_axis():
    """
    Test for rotation around the z-axis which is another case that 
    was affected by the bug.
    """
    x = symbols('x')
    # Create a quaternion representing rotation around the z-axis  
    q = Quaternion(cos(x/2), 0, 0, sin(x/2))
    result = trigsimp(q.to_rotation_matrix())
    
    # The correct matrix should be:
    # [[cos(x), -sin(x), 0],
    #  [sin(x),  cos(x), 0], 
    #  [     0,       0, 1]]
    expected = Matrix([
        [cos(x), -sin(x), 0],
        [sin(x),  cos(x), 0],
        [     0,       0, 1]
    ])
    
    # This should pass with the correct implementation  
    assert result == expected