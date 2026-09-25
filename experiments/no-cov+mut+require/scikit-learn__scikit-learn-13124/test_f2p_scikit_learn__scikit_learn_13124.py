"""
Test for the StratifiedKFold shuffle behavior bug fix.

This test ensures that when shuffle=True, different random_state values
produce genuinely different shuffling behavior across all splits, 
because each KFold instance inside StratifiedKFold now gets its own 
properly initialized random number generator.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_independence_between_random_states():
    """
    The core issue addressed by the fix: 
    When shuffle=True, different random_state values should produce 
    independent random shuffling behavior across all fold splits.
    
    Prior to the fix, using rng = self.random_state would cause 
    multiple KFold instances to share the same random number generator state,
    making different random_state values produce identical results.
    """
    # Use a data set where we can clearly see batch shuffle differences
    X = np.arange(16)  # 16 samples
    y = np.array([0] * 8 + [1] * 8)  # Balanced classes
    
    # Get multiple splits with different but close seeds to increase chance of seeing differences
    skf_low_seed = StratifiedKFold(n_splits=4, shuffle=True, random_state=100)
    skf_high_seed = StratifiedKFold(n_splits=4, shuffle=True, random_state=101)
    
    splits_low = list(skf_low_seed.split(X, y))
    splits_high = list(skf_high_seed.split(X, y))
    
    # At least one fold should differ between the two sets of splits
    # This is the critical test for properly independent random states
    different_folds_found = False
    
    for i, (train_low, test_low) in enumerate(splits_low):
        train_high, test_high = splits_high[i]
        
        # If any train or test sets are different, we're good
        if (not np.array_equal(train_low, train_high) or 
            not np.array_equal(test_low, test_high)):
            different_folds_found = True
            break
    
    # The test passes if different seeds produce different results
    # This would fail if the bug exists (reusing same random state for all KFolds)
    assert different_folds_found, (
        "Different random_state values (100 vs 101) with shuffle=True "
        "should produce different splits, indicating independent random number "
        "generator usage in each KFold instance inside StratifiedKFold. "
        "If they are identical, it indicates a bug in random state handling."
    )


def test_stratified_kfold_deterministic_same_random_state():
    """Ensure that the same random_state always produces the same results."""
    X = np.arange(16)
    y = np.array([0] * 8 + [1] * 8)
    
    # Test that the same random_state produces identical splits
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    
    splits1 = list(skf.split(X, y))
    splits2 = list(skf.split(X, y))
    
    # All folds should be identical
    for i, (train1, test1) in enumerate(splits1):
        train2, test2 = splits2[i]
        assert np.array_equal(train1, train2), f"Train split {i} should be deterministic"
        assert np.array_equal(test1, test2), f"Test split {i} should be deterministic"


def test_stratified_kfold_no_shuffle_deterministic():
    """Ensure shuffle=False produces deterministic results."""
    X = np.arange(16)
    y = np.array([0] * 8 + [1] * 8)
    
    skf = StratifiedKFold(n_splits=4, shuffle=False)
    
    splits1 = list(skf.split(X, y))
    splits2 = list(skf.split(X, y))
    
    # All folds should be identical
    for i, (train1, test1) in enumerate(splits1):
        train2, test2 = splits2[i]
        assert np.array_equal(train1, train2), f"Train split {i} should be deterministic"
        assert np.array_equal(test1, test2), f"Test split {i} should be deterministic"


if __name__ == "__main__":
    test_stratified_kfold_shuffle_independence_between_random_states()
    test_stratified_kfold_deterministic_same_random_state()
    test_stratified_kfold_no_shuffle_deterministic()
    print("All tests passed!")