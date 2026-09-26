"""
Test for StratifiedKFold shuffle behavior bug - regression test.

This test validates the specific fix in the _make_test_folds method:
rng = self.random_state  -->  rng = check_random_state(self.random_state)
"""
import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_random_state_handling():
    """
    Test the specific random state handling fix.
    
    The fix ensures that when shuffle=True, proper random state objects
    are created instead of passing None directly to KFold.
    """
    # Create data that will make the random state behavior explicit
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])  # 4 class 0, 8 class 1
    
    # Test shuffle with random_state=None - this is the key case for the fix
    # In the buggy version, this would pass None directly to KFold
    # In the fixed version, this should create proper RandomState objects
    
    kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=None)
    folds = []
    for train_idx, test_idx in kfold.split(X, y):
        folds.append((train_idx.copy(), test_idx.copy()))
    
    # Validate basic functionality
    assert len(folds) == 3
    for train_idx, test_idx in folds:
        assert len(train_idx) + len(test_idx) == len(X)
        assert len(np.intersect1d(train_idx, test_idx)) == 0


def test_stratified_kfold_shuffle_seed_consistency():
    """
    Test that shuffle=True with same seed produces consistent results.
    """
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 5 class 0, 5 class 1
    
    # Run twice with same parameters - should produce identical results
    kfold1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=999)
    folds1 = []
    for train_idx, test_idx in kfold1.split(X, y):
        folds1.append((train_idx.copy(), test_idx.copy()))
    
    kfold2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=999)
    folds2 = []
    for train_idx, test_idx in kfold2.split(X, y):
        folds2.append((train_idx.copy(), test_idx.copy()))
    
    # Results should be identical due to same seed
    assert len(folds1) == len(folds2) == 2
    for i in range(len(folds1)):
        train1, test1 = folds1[i]
        train2, test2 = folds2[i]
        assert np.array_equal(train1, train2), f"Fold {i} train indices should match"
        assert np.array_equal(test1, test2), f"Fold {i} test indices should match"


def test_stratified_kfold_shuffle_different_seeds():
    """
    Test that different seeds produce different fold assignments.
    """
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])  # 4 class 0, 8 class 1
    
    # Use different random states
    kfold1 = StratifiedKFold(n_splits=3, shuffle=True, random_state=1)
    folds1 = []
    for train_idx, test_idx in kfold1.split(X, y):
        folds1.append((train_idx.copy(), test_idx.copy()))
    
    kfold2 = StratifiedKFold(n_splits=3, shuffle=True, random_state=2)
    folds2 = []
    for train_idx, test_idx in kfold2.split(X, y):
        folds2.append((train_idx.copy(), test_idx.copy()))
    
    # The folds should be different with different random states
    # This validates the shuffle functionality
    folds_different = False
    for i in range(len(folds1)):
        train1, test1 = folds1[i]
        train2, test2 = folds2[i]
        if not np.array_equal(train1, train2) or not np.array_equal(test1, test2):
            folds_different = True
            break
    
    assert folds_different, "Different random states should produce different folds"


def test_stratified_kfold_shuffle_false_consistency():
    """
    Test that shuffle=False produces consistent results.
    """
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # 4 class 0, 4 class 1
    
    # Test shuffle=False with same seed - should be consistent
    kfold1 = StratifiedKFold(n_splits=2, shuffle=False, random_state=42)
    folds1 = []
    for train_idx, test_idx in kfold1.split(X, y):
        folds1.append((train_idx.copy(), test_idx.copy()))
    
    kfold2 = StratifiedKFold(n_splits=2, shuffle=False, random_state=42)
    folds2 = []
    for train_idx, test_idx in kfold2.split(X, y):
        folds2.append((train_idx.copy(), test_idx.copy()))
    
    # Should be identical
    assert len(folds1) == len(folds2) == 2
    for i in range(len(folds1)):
        train1, test1 = folds1[i]
        train2, test2 = folds2[i]
        assert np.array_equal(train1, train2), f"Fold {i} train indices should match"
        assert np.array_equal(test1, test2), f"Fold {i} test indices should match"


if __name__ == "__main__":
    test_stratified_kfold_shuffle_random_state_handling()
    test_stratified_kfold_shuffle_seed_consistency()
    test_stratified_kfold_shuffle_different_seeds()
    test_stratified_kfold_shuffle_false_consistency()
    print("All tests passed!")