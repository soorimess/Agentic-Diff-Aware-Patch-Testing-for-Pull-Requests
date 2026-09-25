"""
Regression test focused on the specific change in StratifiedKFold random state handling.
This tests the core change: replacing rng = self.random_state with rng = check_random_state(self.random_state)
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_random_state_handling():
    """Test that different random_state inputs are handled correctly."""
    X = np.arange(10)
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])  # 5 of each class
    
    # Test with integer random_state
    skf1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    folds1 = list(skf1.split(X, y))
    
    # Test with None random_state - should work without error
    skf2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=None)
    folds2 = list(skf2.split(X, y))
    
    # Basic validation - all should work without error
    assert len(folds1) == 2
    assert len(folds2) == 2
    
    # Each fold should have correct sample counts
    for i in range(2):
        assert len(folds1[i][0]) == len(folds1[i][1]) == 5  # 5 train, 5 test 
        assert len(folds2[i][0]) == len(folds2[i][1]) == 5


def test_stratified_kfold_deterministic_behavior():
    """Test that same random seed produces same result (core behavior)"""
    X = np.arange(10)  
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    
    # Same seed -> same result
    skf1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=12345)
    skf2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=12345)
    
    folds1 = list(skf1.split(X, y))
    folds2 = list(skf2.split(X, y))
    
    assert len(folds1) == len(folds2) == 2
    
    # All folds should be identical
    for i in range(2):
        # Test indices should be identical 
        assert set(folds1[i][1]) == set(folds2[i][1])
        # Train indices should be identical    
        assert set(folds1[i][0]) == set(folds2[i][0])


def test_stratified_kfold_stratification_preserved():
    """Verify that stratification is maintained in all scenarios."""
    X = np.arange(12)
    y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1])  # 6 of each class
    
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=1)
    folds = list(skf.split(X, y))
    
    assert len(folds) == 3
    
    # Verify each fold maintains 2 samples from each class
    for train_idx, test_idx in folds:
        train_y = y[train_idx]
        test_y = y[test_idx] 
        
        # 2 from class 0, 2 from class 1 in train
        assert np.sum(train_y == 0) == 2
        assert np.sum(train_y == 1) == 2
        
        # 2 from class 0, 2 from class 1 in test
        assert np.sum(test_y == 0) == 2
        assert np.sum(test_y == 1) == 2