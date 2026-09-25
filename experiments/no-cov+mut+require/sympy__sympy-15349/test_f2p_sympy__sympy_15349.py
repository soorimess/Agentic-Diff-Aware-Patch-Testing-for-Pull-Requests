from sympy import symbols, trigsimp, cos, sin, Matrix
from sympy.algebras.quaternion import Quaternion

def test_quaternion_rotation_matrix_bug_fix():
    """
    Regression test for bug in Quaternion.to_rotation_matrix() where element [2,1] 
    had wrong sign (sin(x) instead of -sin(x) for x-axis rotation).
    
    The bug fix changes m12 = 2*s*(q.c*q.d + q.b*q.a) to m12 = 2*s*(q.c*q.d - q.b*q.a)
    which corrects the sign in the rotation matrix elements.
    """
    x = symbols('x')
    # Quaternion representing rotation around x-axis (standard convention)
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # Simplify it 
    simplified = trigsimp(matrix)
    
    # The bug causes element [2,1] to be sin(x) instead of -sin(x)
    # This is the exact issue described in the GitHub report
    element_21 = simplified[2, 1]
    
    # With the fix applied, this element should be -sin(x)
    # Without the fix (the buggy behavior), it is sin(x)
    assert element_21 == -sin(x), f"Element [2,1] should be -sin(x) after fix, but got {element_21}"
    
    # Verify the entire matrix structure is correct
    correct_matrix = Matrix([
        [1, 0, 0],
        [0, cos(x), sin(x)], 
        [0, -sin(x), cos(x)]
    ])
    
    assert simplified == correct_matrix, "Matrix should match corrected form for x-axis rotation"

def test_quaternion_to_rotation_matrix_m12_fix():
    """
    Direct test for the specific m12 element calculation fix.
    The fix changes m12 from using addition to subtraction in its computation.
    """
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    matrix = q.to_rotation_matrix()
    simplified = trigsimp(matrix)
    
    # Element [1,2] is the m12 element from the matrix computation
    # Before fix: m12 = 2*s*(q.c*q.d + q.b*q.a) = sin(x) 
    # After fix:  m12 = 2*s*(q.c*q.d - q.b*q.a) = -sin(x)
    #
    # So this element should now be -sin(x) not sin(x)
    m12_element = simplified[1, 2] 
    
    # After fix, this should be -sin(x) = -sin(x) 
    assert m12_element == -sin(x), "m12 element should be -sin(x) after fix"