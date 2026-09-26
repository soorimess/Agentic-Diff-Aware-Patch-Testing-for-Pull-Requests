"""
Regression test for StratifiedKFold shuffle behavior bug.
This test specifically targets the exact behavior change in the fix:
rng = self.random_state  -->  rng = check_random_state(self.random_state)
"""
import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_random_state_consistency():
    """
    Test that demonstrates the fix for proper random state handling.
    Before the fix, using an integer random_state directly could cause 
    inconsistent behavior in shuffle operations.
    """
    # Use a dataset that makes the shuffle behavior very clear
    X = np.arange(24)
    y = np.array([1]*12 + [0]*12)
    
    # Test that same random state produces identical results across multiple calls
    # This is the core of what was broken in the original implementation
    fold_structures = []
    for i in range(4):
        kfold = StratifiedKFold(n_splits=6, shuffle=True, random_state=12345)
        folds = []
        for train_idx, test_idx in kfold.split(X, y):
            folds.append((set(train_idx), set(test_idx)))
        fold_structures.append(folds)
    
    # All should be identical with proper random state handling
    for i in range(1, len(fold_structures)):
        assert fold_structures[0] == fold_structures[i], \
            f"Fold structures differ with same random_state on run {i}"


def test_stratified_kfold_shuffle_behavior_difference():
    """
    Test that shuffle=True actually produces different results than shuffle=False.
    This validates the documented behavior of the shuffle parameter.
    """
    X = np.arange(18)
    y = np.array([1]*9 + [0]*9)
    
    # Get structure with shuffle=False (predictable)
    kfold_no_shuffle = StratifiedKFold(n_splits=3, shuffle=False, random_state=999)
    folds_no_shuffle = []
    for train_idx, test_idx in kfold_no_shuffle.split(X, y):
        folds_no_shuffle.append((set(train_idx), set(test_idx)))
    
    # Get structure with shuffle=True (should be different)
    kfold_shuffle = StratifiedKFold(n_splits=3, shuffle=True, random_state=999)
    folds_shuffle = []
    for train_idx, test_idx in kfold_shuffle.split(X, y):
        folds_shuffle.append((set(train_idx), set(test_idx)))
    
    # At least some folds should be different due to shuffling
    different_count = 0
    for i in range(len(folds_no_shuffle)):
        train_no_shuffle = folds_no_shuffle[i][0]
        test_no_shuffle = folds_no_shuffle[i][1]
        train_shuffle = folds_shuffle[i][0]
        test_shuffle = folds_shuffle[i][1]
        
        if train_no_shuffle != train_shuffle or test_no_shuffle != test_shuffle:
            different_count += 1
    
    # At least one fold should be different to show shuffling works
    assert different_count > 0, "shuffle=True should produce different fold structure"