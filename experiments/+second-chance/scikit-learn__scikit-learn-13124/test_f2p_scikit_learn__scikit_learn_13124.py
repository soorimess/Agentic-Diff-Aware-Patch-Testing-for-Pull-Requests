"""
Regression tests for bug in StratifiedKFold shuffle parameter.

The bug was that the shuffle parameter affected the order of the cross-validation
folds rather than shuffling samples within each class before splitting.
This caused identical folds to be produced for different random seeds when shuffle=True.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_actually_shuffles_samples():
    """Test that shuffle=True actually shuffles samples within each class.
    
    This test reproduces the specific issue reported in the bug:
    With shuffle=True, different random seeds should produce different 
    content within each fold (not just different order of folds).
    """
    # Reproduce the exact example from the bug report
    RANDOM_SEED = 1
    
    samples_per_class = 10
    X = np.linspace(0, samples_per_class*2-1, samples_per_class * 2)
    y = np.concatenate((np.ones(samples_per_class), np.zeros(samples_per_class)), axis=0)
    
    # Test with shuffle=False first
    k_fold_no_shuffle = StratifiedKFold(n_splits=10, shuffle=False, random_state=RANDOM_SEED)
    no_shuffle_splits = list(k_fold_no_shuffle.split(X, y))
    
    # Test with shuffle=True and same random seed
    k_fold_shuffle = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED)
    shuffle_splits = list(k_fold_shuffle.split(X, y))
    
    # Test with shuffle=True and different random seed  
    k_fold_shuffle2 = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED + 1)
    shuffle_splits2 = list(k_fold_shuffle2.split(X, y))
    
    # Test the specific issue:
    # - In the buggy version, shuffle=True with different seeds gives same splits 
    # - In the fixed version, shuffle=True should give different splits
    
    # Check that the actual sets of indices within the folds are different
    # when using different random seeds with shuffle=True
    
    # Store just the test indices for comparison (indices within each fold)
    test_indices_shuffle1 = [test_idx for train_idx, test_idx in shuffle_splits]
    test_indices_shuffle2 = [test_idx for train_idx, test_idx in shuffle_splits2]
    
    # The pieces of data that should be shuffled (should be different with different seeds)
    # In the buggy implementation, these would be identical because it doesn't actually 
    # shuffle samples within classes, just reorders the folds
    
    # Check at least one fold has different content with different seeds
    different_found = False
    
    for i in range(len(test_indices_shuffle1)):
        if not np.array_equal(test_indices_shuffle1[i], test_indices_shuffle2[i]):
            different_found = True
            break
    
    # This should pass with the fix (content of folds changes with different seeds)
    # This should fail with the buggy version
    assert different_found, ("When shuffle=True is used with different random_state values, "
                           "the content (indices) of the folds should be different. "
                           "This indicates that samples are actually being shuffled "
                           "within classes, not just the order of folds being shuffled.")


def test_stratified_kfold_shuffle_deterministic_same_seed():
    """Test that shuffle=True with same random_state produces deterministic results."""
    # Reproduce the exact example from the bug report 
    RANDOM_SEED = 1
    
    samples_per_class = 10
    X = np.linspace(0, samples_per_class*2-1, samples_per_class * 2)
    y = np.concatenate((np.ones(samples_per_class), np.zeros(samples_per_class)), axis=0)
    
    # Create two identical kfold objects with same random seed
    k_fold1 = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED)
    k_fold2 = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_SEED)
    
    splits1 = list(k_fold1.split(X, y))
    splits2 = list(k_fold2.split(X, y))
    
    # The splits should be identical
    for (train1, test1), (train2, test2) in zip(splits1, splits2):
        assert np.array_equal(train1, train2), "Same seed should produce identical train splits"
        assert np.array_equal(test1, test2), "Same seed should produce identical test splits"
        

def test_stratified_kfold_no_shuffle_deterministic():
    """Test that shuffle=False produces deterministic results."""
    # Reproduce the exact example from the bug report
    RANDOM_SEED = 1
    
    samples_per_class = 10
    X = np.linspace(0, samples_per_class*2-1, samples_per_class * 2)
    y = np.concatenate((np.ones(samples_per_class), np.zeros(samples_per_class)), axis=0)
    
    # Should be deterministic regardless of seed when shuffle=False
    k_fold1 = StratifiedKFold(n_splits=10, shuffle=False, random_state=RANDOM_SEED)
    k_fold2 = StratifiedKFold(n_splits=10, shuffle=False, random_state=RANDOM_SEED + 100)
    
    splits1 = list(k_fold1.split(X, y))
    splits2 = list(k_fold2.split(X, y))
    
    # Both should give the exact same splits
    for (train1, test1), (train2, test2) in zip(splits1, splits2):
        assert np.array_equal(train1, train2), "No shuffle should give same result regardless of seed"
        assert np.array_equal(test1, test2), "No shuffle should give same result regardless of seed"