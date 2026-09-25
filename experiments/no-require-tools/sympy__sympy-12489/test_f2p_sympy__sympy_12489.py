"""Test for Permutation subclassing regression."""

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import Cycle


class MyPermutation(Permutation):
    """A subclass of Permutation for testing purposes."""
    
    def is_my_permutation(self):
        return True


def test_permutation_subclassing_creation():
    """Test that various Permutation creation methods preserve subclass."""
    # Test 1: Basic creation from list 
    p1 = MyPermutation([0, 2, 1])
    assert isinstance(p1, MyPermutation)
    assert p1.is_my_permutation()
    
    # Test 2: Creation from cycle 
    p2 = MyPermutation([[0, 1], [2, 3]])  
    assert isinstance(p2, MyPermutation)
    assert p2.is_my_permutation()
    
    # Test 3: Copy from existing permutation
    p3 = MyPermutation([1, 0, 2])
    p4 = MyPermutation(p3)
    assert isinstance(p4, MyPermutation)
    assert p4.is_my_permutation()
    
    # Test 4: Creation from single integer
    p5 = MyPermutation(3)  # Should create [0, 1, 2, 3] 
    assert isinstance(p5, MyPermutation)
    assert p5.is_my_permutation()
    
    # Test 5: Creation with size parameter
    p6 = MyPermutation([0, 2, 1], size=5) 
    assert isinstance(p6, MyPermutation)
    assert p6.is_my_permutation()
    
    # Test 6: Creation with no arguments (empty permutation)
    p7 = MyPermutation()
    assert isinstance(p7, MyPermutation)
    assert p7.is_my_permutation()
    
    # Test 7: Creation with multiple arguments (should convert to cycles)
    p8 = MyPermutation(1, 2, 3)
    assert isinstance(p8, MyPermutation)
    assert p8.is_my_permutation()


def test_permutation_operations_preserve_subclass():
    """Test that permutation operations preserve subclass type."""
    p1 = MyPermutation([0, 2, 1])
    p2 = MyPermutation([1, 0, 2])
    
    # Multiplication of two subclass instances  
    result1 = p1 * p2
    assert isinstance(result1, MyPermutation)
    assert result1.is_my_permutation()
    
    # Inversion (bitwise not)
    result2 = ~p1
    assert isinstance(result2, MyPermutation)
    assert result2.is_my_permutation()
    
    # Power operation  
    result3 = p1 ** 2
    assert isinstance(result3, MyPermutation)
    assert result3.is_my_permutation()
    
    # Addition (change rank)
    result4 = p1 + 1
    assert isinstance(result4, MyPermutation)
    assert result4.is_my_permutation()
    
    # Test behavior via component operations that were affected
    # Conversion with full cycle
    p3 = MyPermutation([[1, 2]])
    result5 = p1 * p3
    assert isinstance(result5, MyPermutation)
    assert result5.is_my_permutation()


def test_permutation_rmul_preserves_subclass():
    """Test that right multiplication preserves subclass type."""
    p1 = MyPermutation([0, 2, 1])
    
    # Right multiplication with regular Permutation should still return subclass
    result = Permutation([1, 0, 2]) * p1
    assert isinstance(result, MyPermutation)
    assert result.is_my_permutation()
    
    # Check again ensuring that even when we create instances differently
    p2 = Permutation([0, 1, 2])
    result2 = p2 * p1
    assert isinstance(result2, MyPermutation)
    assert result2.is_my_permutation()