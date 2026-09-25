"""
Regression test for Quaternion.to_rotation_matrix() bug.

The bug was in line 532 of sympy/algebras/quaternion.py where the sign
was incorrect in the m12 value of the rotation matrix.

Before fix: m12 = 2*s*(q.c*q.d + q.b*q.a)
After fix:  m12 = 2*s*(q.c*q.d - q.b*q.a)
"""

from sympy import symbols, cos, sin, Matrix, trigsimp
from sympy.algebras.quaternion import Quaternion

def test_quaternion_to_rotation_matrix_bug():
    """Test for the specific bug in to_rotation_matrix where m12 had wrong sign"""
    x = symbols('x')
    
    # Create a quaternion representing rotation about x-axis
    # This is the example from the bug report
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The expected matrix should have -sin(x) in position (1,2)
    # Not sin(x) as incorrectly computed before the fix
    expected_matrix = Matrix([
        [1,      0,      0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    
    # Using trigsimp to simplify the trigonometric expressions
    actual_matrix = trigsimp(matrix)
    
    # Assert that the actual result matches what we expect
    assert actual_matrix == expected_matrix

def test_quaternion_to_rotation_matrix_y_axis():
    """Test that the fix also works with rotation about y-axis"""
    x = symbols('x')
    
    # Create a quaternion representing rotation about y-axis
    q = Quaternion(cos(x/2), 0, sin(x/2), 0)
    
    # Get the rotation matrix 
    matrix = q.to_rotation_matrix()
    
    # The expected matrix should have sin(x) in position (0,2) but -sin(x) in position (2,0)
    expected_matrix = Matrix([
        [cos(x), 0, sin(x)],
        [0,      1, 0],
        [-sin(x), 0, cos(x)]
    ])
    
    # Using trigsimp to simplify the trigonometric expressions
    actual_matrix = trigsimp(matrix)
    
    # Assert that the actual result matches what we expect
    assert actual_matrix == expected_matrix

def test_quaternion_to_rotation_matrix_z_axis():
    """Test that the fix also works with rotation about z-axis"""
    x = symbols('x')
    
    # Create a quaternion representing rotation about z-axis
    q = Quaternion(cos(x/2), 0, 0, sin(x/2))
    
    # Get the rotation matrix
    matrix = q.to_rotation_matrix()
    
    # The expected matrix should have -sin(x) in position (0,1) 
    expected_matrix = Matrix([
        [cos(x), -sin(x), 0],
        [sin(x), cos(x),  0],
        [0,      0,      1]
    ])
    
    # Using trigsimp to simplify the trigonometric expressions
    actual_matrix = trigsimp(matrix)
    
    # Assert that the actual result matches what we expect
    assert actual_matrix == expected_matrix