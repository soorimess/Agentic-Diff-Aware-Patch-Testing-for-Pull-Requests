from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_to_rotation_matrix_off_diagonal_signs():
    """Test that the off-diagonal elements of rotation matrix have correct signs.
    
    The bug was in the calculation of m12 element in to_rotation_matrix.
    In the case of rotation about x-axis, the matrix should be:
    [[1, 0, 0],
     [0, cos(x), -sin(x)],
     [0, sin(x), cos(x)]]
    
    But due to the bug, it was producing:
    [[1, 0, 0],
     [0, cos(x), sin(x)],
     [0, sin(x), cos(x)]]
    """
    x = symbols('x')
    # Create a quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    result = q.to_rotation_matrix()
    
    # The matrix should have -sin(x) in position (1,2) and sin(x) in position (2,1)
    # Not both sin(x) as in the buggy version
    result_trigsimp = trigsimp(result)
    
    # Extract the specific elements
    m12 = result_trigsimp[1, 2]  # Should be -sin(x)
    m21 = result_trigsimp[2, 1]  # Should be sin(x)
    
    # Check that they have the correct relationship
    # m12 should be -sin(x) and m21 should be sin(x)
    assert m12 == -sin(x), f"Expected m12 to be -sin(x), got {m12}"
    assert m21 == sin(x), f"Expected m21 to be sin(x), got {m21}"