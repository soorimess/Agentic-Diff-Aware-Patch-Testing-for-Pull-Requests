"""
Regression test for StratifiedKFold shuffle behavior bug.

The bug was that when shuffle=True, samples within each class were not properly 
shuffled due to incorrect random state handling in _make_test_folds.
The fix was to change rng = self.random_state to rng = check_random_state(self.random_state).
"""
import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_ensures_randomization():
    """
    Test that shuffle=True ensures proper randomization of samples within classes.
    
    This test verifies that different random seeds produce different fold assignments,
    which is the core behavior that the fix addresses.
    """
    # Use a test case that makes the difference obvious
    X = np.arange(10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 5 samples each class
    
    # Get splits with two different random states
    kfold1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=100)
    kfold2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=200)
    
    splits1 = list(kfold1.split(X, y))
    splits2 = list(kfold2.split(X, y))
    
    # Verify we have the expected number of splits
    assert len(splits1) == len(splits2) == 2
    
    # The key test: different random states should produce different splits
    # This validates that the shuffle is actually working on the samples
    different = False
    for (train1, test1), (train2, test2) in zip(splits1, splits2):
        if not np.array_equal(train1, train2) or not np.array_equal(test1, test2):
            different = True
            break
    
    # This assertion would fail if shuffle was broken (same results for different seeds)
    assert different, (
        "Different random states should produce different fold structures when shuffle=True. "
        "This demonstrates that the shuffle functionality works correctly."
    )


def test_stratified_kfold_shuffle_false_consistency():
    """Test that shuffle=False produces consistent results."""
    X = np.arange(10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    
    kfold1 = StratifiedKFold(n_splits=2, shuffle=False, random_state=42)
    kfold2 = StratifiedKFold(n_splits=2, shuffle=False, random_state=42)
    
    splits1 = list(kfold1.split(X, y))
    splits2 = list(kfold2.split(X, y))
    
    # With shuffle=False and same random_state, results should be identical
    for (train1, test1), (train2, test2) in zip(splits1, splits2):
        assert np.array_equal(train1, train2), "Same random_state should produce same train indices"
        assert np.array_equal(test1, test2), "Same random_state should produce same test indices"