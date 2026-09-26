from sympy.algebras.quaternion import Quaternion
from sympy import symbols, trigsimp, cos, sin

def test_quaternion_rotation_matrix_signs():
    """
    Test that verifies the fix for Quaternion.to_rotation_matrix() bug.
    
    The bug was in the computation of matrix elements m12 and m21 which had 
    incorrect signs. For a rotation about the x-axis, these should be -sin(x).
    """
    x = symbols('x')
    # Create quaternion for x-axis rotation (from bug report example)
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get rotation matrix
    result = q.to_rotation_matrix()
    simplified = trigsimp(result)
    
    # The bug causes these elements to be sin(x) instead of -sin(x)
    # The test asserts the correct (fixed) behavior
    m12 = simplified[1, 2]  # Should be -sin(x)
    m21 = simplified[2, 1]  # Should be -sin(x)
    
    # These assertions should pass with the fix applied
    # They fail with the bug present (which is correct behavior for this test)
    assert m12 == -sin(x), f"m12 should be -sin(x) but got {m12}"
    assert m21 == -sin(x), f"m21 should be -sin(x) but got {m21}"

if __name__ == "__main__":
    test_quaternion_rotation_matrix_signs()