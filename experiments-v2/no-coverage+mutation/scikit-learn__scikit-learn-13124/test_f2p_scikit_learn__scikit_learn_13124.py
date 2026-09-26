"""
Test for StratifiedKFold shuffle behavior bug.

This test verifies that when shuffle=True, the samples within each class
are properly shuffled before splitting into folds.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_with_different_seeds():
    """
    Test that shuffle=True with different random seeds produces different results.
    
    This is the core bug: when shuffle=True, different random seeds should 
    produce different fold structures, but due to improper random state handling,
    they don't.
    """
    # Create a dataset with clear pattern
    X = np.arange(10)
    y = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])  # 5 ones, 5 zeros
    
    # Get results with seed 1
    kfold_seed1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=1)
    folds_seed1 = []
    for train_idx, test_idx in kfold_seed1.split(X, y):
        folds_seed1.append((train_idx, test_idx))
    
    # Get results with seed 2
    kfold_seed2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=2)
    folds_seed2 = []
    for train_idx, test_idx in kfold_seed2.split(X, y):
        folds_seed2.append((train_idx, test_idx))
    
    # With proper shuffle, these should be different
    # The bug is that the same indices appear regardless of random_state
    # Check that at least one fold has different indices
    different = False
    for i in range(len(folds_seed1)):
        if not np.array_equal(folds_seed1[i][0], folds_seed2[i][0]):
            different = True
            break
        if not np.array_equal(folds_seed1[i][1], folds_seed2[i][1]):
            different = True
            break
    
    # This should be True with proper shuffle implementation
    # If it's False, that means shuffle isn't working properly
    # which is the bug we're testing for
    assert different, "Different random states should produce different fold structures"


def test_stratified_kfold_shuffle_vs_no_shuffle():
    """
    Test that shuffle=True and shuffle=False produce different results.
    
    This tests the exact issue described in the bug report where shuffle=True
    was not actually shuffling samples within classes.
    """
    X = np.arange(10)
    y = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
    
    # Get results with shuffle=False
    kfold_no_shuffle = StratifiedKFold(n_splits=2, shuffle=False, random_state=1)
    folds_no_shuffle = []
    for train_idx, test_idx in kfold_no_shuffle.split(X, y):
        folds_no_shuffle.append((train_idx, test_idx))
    
    # Get results with shuffle=True  
    kfold_shuffle = StratifiedKFold(n_splits=2, shuffle=True, random_state=1)
    folds_shuffle = []
    for train_idx, test_idx in kfold_shuffle.split(X, y):
        folds_shuffle.append((train_idx, test_idx))
    
    # With proper shuffle, these should be different
    # The bug is that shuffle=True produces the same result as shuffle=False
    
    # Check if any fold has different indices
    different = False
    for i in range(len(folds_no_shuffle)):
        if not np.array_equal(folds_no_shuffle[i][0], folds_shuffle[i][0]):
            different = True
            break
        if not np.array_equal(folds_no_shuffle[i][1], folds_shuffle[i][1]):
            different = True
            break
    
    # This assertion should fail with the buggy implementation
    # because shuffle=True should produce different results from shuffle=False
    assert different, "shuffle=True should produce different results than shuffle=False"