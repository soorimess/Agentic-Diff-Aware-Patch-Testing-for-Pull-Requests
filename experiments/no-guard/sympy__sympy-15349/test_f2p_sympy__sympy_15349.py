from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin, Matrix

def test_quaternion_to_rotation_matrix_m12_sign_bug():
    """Test for the specific bug in Quaternion.to_rotation_matrix() m12 element sign.
    
    The bug was in line m12 = 2*s*(q.c*q.d + q.b*q.a) which should be
    m12 = 2*s*(q.c*q.d - q.b*q.a). This affects the sign of sin(x) in 
    rotation matrices for specific quaternion constructs.
    """
    x = symbols('x')
    
    # Create a quaternion representing rotation about x-axis  
    # This specific case demonstrates the bug in m12 element calculation
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix and simplify
    result = trigsimp(q.to_rotation_matrix())
    
    # The bug was in the m12 element (row 1, col 2) of the resulting matrix
    # Before fix: m12 = 2*s*(0*0 + sin(x/2)*cos(x/2)) = sin(x) (wrong sign)
    # After fix:  m12 = 2*s*(0*0 - sin(x/2)*cos(x/2)) = -sin(x) (correct) 
    assert result[1, 2] == -sin(x), f"Element at (1,2) should be -sin(x), got {result[1, 2]}"

def test_quaternion_to_rotation_matrix_correct_matrix_structure():
    """Test the complete matrix structure to confirm the fix works properly."""
    x = symbols('x')
    
    # Create a quaternion representing rotation about x-axis
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix and simplify
    result = trigsimp(q.to_rotation_matrix())
    
    # Expected result for rotation about x-axis (correct behavior):
    expected = Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],  # Note: -sin(x) in position (1,2) - this is the key fix
        [0, sin(x), cos(x)]
    ])
    
    # Check key elements that were problematic based on the bug fix
    assert result[1, 2] == -sin(x), "Position (1,2) should be -sin(x) - this tests the specific bug"
    assert result[0, 0] == 1, "Position (0,0) should be 1"
    assert result[1, 1] == cos(x), "Position (1,1) should be cos(x)"
    assert result[2, 1] == sin(x), "Position (2,1) should be sin(x)"