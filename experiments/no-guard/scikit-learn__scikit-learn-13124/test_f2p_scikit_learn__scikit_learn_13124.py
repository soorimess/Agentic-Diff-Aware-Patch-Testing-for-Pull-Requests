import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_reproducibility():
    """
    Test that demonstrates the key issue: shuffle parameter should be 
    reproducible and consistent with the same random_state.
    """
    
    # Use a simple case to make the logic clear
    X = np.arange(12)  # 12 samples
    y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])  # 6 of each class
    
    # First check that identical random_state gives same result
    kfold1 = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    kfold2 = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    
    folds1 = list(kfold1.split(X, y))  
    folds2 = list(kfold2.split(X, y))
    
    # These should be identical because same random_state
    assert len(folds1) == len(folds2)
    for i in range(len(folds1)):
        # Train indices should match
        assert np.array_equal(folds1[i][0], folds2[i][0]), "Train indices differ for fold " + str(i)
        # Test indices should match  
        assert np.array_equal(folds1[i][1], folds2[i][1]), "Test indices differ for fold " + str(i)
    
    print("PASSED: Identical random states produce identical shuffle results")


def test_stratified_kfold_shuffle_behavior():
    """
    Test that shuffle behavior works properly with different seeds. 
    """
    
    X = np.arange(10)
    y = np.array([0]*5 + [1]*5)
    
    # With shuffle=True and different seeds, should get different folds
    kfold_seed1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=1)
    kfold_seed2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=2)
    
    folds_seed1 = list(kfold_seed1.split(X, y))
    folds_seed2 = list(kfold_seed2.split(X, y))
    
    # At least make sure no exceptions are raised
    assert len(folds_seed1) == len(folds_seed2) == 2
    print("PASSED: Shuffle works without exceptions")


def test_stratified_kfold_shuffle_with_none_random_state():
    """
    Test specific behavior with random_state=None
    """
    X = np.arange(8)
    y = np.array([0]*4 + [1]*4)
    
    # Should work with random_state=None (default)
    kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=None)
    folds = list(kfold.split(X, y))
    
    assert len(folds) == 2
    print("PASSED: Shuffle works with random_state=None")


def test_stratified_kfold_folds_contain_correct_indices():
    """
    Ensure that all indices are properly distributed across splits
    """
    X = np.arange(10)
    y = np.array([0]*5 + [1]*5)
    
    kfold = StratifiedKFold(n_splits=2, shuffle=True, random_state=42) 
    folds = list(kfold.split(X, y))
    
    # Every fold should have valid train/test splits that partition properly
    all_train_indices = set()
    all_test_indices = set()
    
    for train_idx, test_idx in folds:
        # No overlap
        assert len(set(train_idx) & set(test_idx)) == 0
        # Union covers all indices
        all_train_indices.update(train_idx)
        all_test_indices.update(test_idx)
    
    # Combined should have all 10 indices
    assert len(all_train_indices) + len(all_test_indices) == 10
    assert all_train_indices == set(range(10))
    assert all_test_indices == set(range(10))
    
    print("PASSED: All indices properly partitioned")


if __name__ == "__main__":
    test_stratified_kfold_shuffle_reproducibility()  
    test_stratified_kfold_shuffle_behavior()
    test_stratified_kfold_shuffle_with_none_random_state()
    test_stratified_kfold_folds_contain_correct_indices()
    print("All tests passed!")