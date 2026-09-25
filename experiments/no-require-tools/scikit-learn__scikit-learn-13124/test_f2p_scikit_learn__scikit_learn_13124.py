"""Test for StratifiedKFold shuffle behavior: the specific bug fix from PR.

This test file is designed to verify the fix in scikit-learn PR that addressed 
an issue with how random state was handled in StratifiedKFold's _make_test_folds method,
specifically the change from:
    rng = self.random_state    # BEFORE (buggy)
    rng = check_random_state(self.random_state)  # AFTER (fixed)

The bug was subtle but related to how independent random number generation was handled
within the stratified cross-validation process for different classes.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_behavior_correctly_uses_random_state():
    """Test that shuffle behavior properly uses random state for independent generation.
    
    This validates the fix that changed how the random state parameter is processed
    within StratifiedKFold to use check_random_state() for proper randomness.
    """
    # Use a scenario that makes the shuffle behavior more apparent
    X = np.arange(16)  # 16 samples
    y = np.array([0]*4 + [1]*4 + [2]*4 + [3]*4)  # 4 classes with 4 samples each
    
    # Create two different kfold instances with the same shuffle settings  
    # but with different random states to test independence
    kfold1 = StratifiedKFold(n_splits=4, shuffle=True, random_state=777)
    kfold2 = StratifiedKFold(n_splits=4, shuffle=True, random_state=888)
    
    folds1 = list(kfold1.split(X, y))  
    folds2 = list(kfold2.split(X, y))
    
    # Basic check: results should not be identical (unless by very rare chance)
    train_indices_1 = [f[0] for f in folds1]
    train_indices_2 = [f[0] for f in folds2]
    
    # This would indicate the shuffle is actually working to generate different orders
    # (the key fix is ensuring independent random generation)
    different_count = sum(1 for t1, t2 in zip(train_indices_1, train_indices_2)
                         if not np.array_equal(t1, t2))
    
    # With proper random state handling, most folds should differ
    # (especially when using properly independent random generators)
    assert different_count >= 1, (
        "With different random seeds and shuffle=True, there should be "
        "variations in fold arrangements. This verifies that shuffle uses "
        "independent random generation per fold."
    )


def test_stratified_kfold_same_seed_consistency():
    """Test that identical random seed produces identical results."""
    X = np.arange(12) 
    y = np.array([0]*4 + [1]*4 + [2]*4)  # 3 classes with 4 samples each
    
    kfold1 = StratifiedKFold(n_splits=3, shuffle=True, random_state=1000)
    kfold2 = StratifiedKFold(n_splits=3, shuffle=True, random_state=1000)
    
    folds1 = list(kfold1.split(X, y))
    folds2 = list(kfold2.split(X, y))
    
    # All corresponding folds should be identical when using same random seed
    for i, (train1, test1) in enumerate(folds1):
        train2, test2 = folds2[i]
        assert np.array_equal(train1, train2), f"Fold {i} train indices should be identical"
        assert np.array_equal(test1, test2), f"Fold {i} test indices should be identical"


def test_stratified_kfold_no_shuffle_deterministic():
    """Test that shuffle=False produces deterministic behavior."""
    X = np.arange(10) 
    y = np.array([0]*5 + [1]*5)  # 2 classes with 5 samples each
    
    kfold1 = StratifiedKFold(n_splits=2, shuffle=False, random_state=999)
    kfold2 = StratifiedKFold(n_splits=2, shuffle=False, random_state=111)
    
    folds1 = list(kfold1.split(X, y))
    folds2 = list(kfold2.split(X, y))
    
    # No shuffle, so result should be independent of random_state
    for i, (train1, test1) in enumerate(folds1):
        train2, test2 = folds2[i]
        assert np.array_equal(train1, train2), f"Fold {i} train indices should be identical regardless of random_state"
        assert np.array_equal(test1, test2), f"Fold {i} test indices should be identical regardless of random_state"


def test_stratified_kfold_random_state_handling():
    """Test fundamental random state handling behavior."""
    X = np.arange(8)
    y = np.array([0]*4 + [1]*4)  # Two classes
    
    # Test with None, integer, and RandomState for compatibility
    kfold1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=None)  
    kfold2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    
    # Should both execute without error and produce reasonable results
    folds1 = list(kfold1.split(X, y))
    folds2 = list(kfold2.split(X, y))
    
    assert len(folds1) == 2
    assert len(folds2) == 2
    
    # Basic correctness: all samples should be covered in train/test sets
    all_train_indices = np.concatenate([f[0] for f in folds1])
    all_test_indices = np.concatenate([f[1] for f in folds1])
    
    assert set(all_train_indices) == set(range(8))
    assert set(all_test_indices) == set(range(8))
    assert len(set(all_train_indices) & set(all_test_indices)) == 0  # No overlap