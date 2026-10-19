"""
Test for batched input support in linalg.eig (PR #21462)

This test ensures that the eig function now properly supports batched inputs
where arrays can have additional "batch" dimensions prepended to their core shape.
"""
import numpy as np
import pytest
from scipy import linalg


def test_eig_batched_input_shape():
    """Test that eig properly handles batched 2D matrix inputs and returns correct shapes."""
    # Create a batch of 2x2 matrices - this should work after the fix
    batch_shape = (2, 3)
    core_shape = (2, 2)
    input_shape = batch_shape + core_shape
    
    # Create batch of matrices 
    matrices = np.random.rand(*input_shape)
    
    # This should work after the decorator is applied
    # The result should have shape (2, 3, 2) for eigenvalues and (2, 3, 2, 2) for eigenvectors
    evals, evecs = linalg.eig(matrices)
    
    # Check that output has correct batched shapes
    assert evals.shape == batch_shape + (2,)  # eigenvalues shape: (2, 3, 2)
    assert evecs.shape == batch_shape + (2, 2)  # eigenvectors shape: (2, 3, 2, 2)
    
    # Verify that we get the right number of eigenvalues/eigenvectors for each matrix in batch
    assert evals.shape[0] == 2
    assert evals.shape[1] == 3
    assert evals.shape[2] == 2
    
    assert evecs.shape[0] == 2
    assert evecs.shape[1] == 3
    assert evecs.shape[2] == 2
    assert evecs.shape[3] == 2


def test_eig_single_matrix():
    """Test that eig still works with single 2D matrices (regression test)."""
    # Single 2x2 matrix
    matrix = np.array([[1.0, 2.0], [3.0, 4.0]])
    
    evals, evecs = linalg.eig(matrix)
    
    # Check that we get the right shapes
    assert evals.shape == (2,)
    assert evecs.shape == (2, 2)
    
    # Check that eigenvalue equation holds: A*v = lambda*v
    for i in range(2):
        Av = matrix @ evecs[:, i]
        lambda_v = evals[i] * evecs[:, i]
        np.testing.assert_allclose(Av, lambda_v, rtol=1e-10)


def test_eig_batched_with_b():
    """Test that eig supports batched inputs for generalized eigenvalue problem."""
    # Create batch of 2x2 matrices for generalized eigenvalue problem
    batch_shape = (2, 2)
    core_shape = (2, 2)
    input_shape = batch_shape + core_shape
    
    # Create batch of matrices
    a_matrices = np.random.rand(*input_shape)
    b_matrices = np.random.rand(*input_shape)
    
    evals, evecs = linalg.eig(a_matrices, b=b_matrices)
    
    # Check that output has correct shape
    assert evals.shape == batch_shape + (2,)  # eigenvalues shape
    assert evecs.shape == batch_shape + (2, 2)  # eigenvectors shape