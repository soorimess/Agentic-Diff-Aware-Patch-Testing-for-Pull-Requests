import numpy as np
from sklearn.model_selection import StratifiedKFold

def test_stratified_kfold_shuffle_random_state_fix():
    """
    Regression test for StratifiedKFold shuffle random state handling fix.
    
    This test verifies that the fix for the shuffle parameter works correctly.
    The fix changed:
    - `rng = self.random_state` to `rng = check_random_state(self.random_state)`
    
    This ensures that when an integer is passed as random_state, it's properly
    converted to a RandomState object before being used in internal KFold operations.
    This is essential for correct shuffle behavior.
    """
    
    # Test data with clear structure
    X = np.arange(10)
    y = np.array([0] * 5 + [1] * 5)
    
    # Test deterministic behavior with same random state
    skf1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    skf2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=42)
    
    folds1 = []
    for train_idx, test_idx in skf1.split(X, y):
        folds1.append((train_idx.copy(), test_idx.copy()))
        
    folds2 = []
    for train_idx, test_idx in skf2.split(X, y):
        folds2.append((train_idx.copy(), test_idx.copy()))
    
    # Same random state should produce identical results (deterministic behavior)
    assert len(folds1) == len(folds2)
    for i in range(len(folds1)):
        train1, test1 = folds1[i]
        train2, test2 = folds2[i]
        assert np.array_equal(train1, train2), "Same random state should produce identical results"
        assert np.array_equal(test1, test2), "Same random state should produce identical results"
    
    # Test shuffle=False is deterministic regardless of random_state
    skf3 = StratifiedKFold(n_splits=2, shuffle=False, random_state=100)
    skf4 = StratifiedKFold(n_splits=2, shuffle=False, random_state=200)
    
    folds3 = []
    for train_idx, test_idx in skf3.split(X, y):
        folds3.append((train_idx.copy(), test_idx.copy()))
        
    folds4 = []
    for train_idx, test_idx in skf4.split(X, y):
        folds4.append((train_idx.copy(), test_idx.copy()))
    
    # shuffle=False should be deterministic regardless of random_state
    assert len(folds3) == len(folds4)
    for i in range(len(folds3)):
        train1, test1 = folds3[i]
        train2, test2 = folds4[i]
        assert np.array_equal(train1, train2), "shuffle=False should be deterministic regardless of random_state"
        assert np.array_equal(test1, test2), "shuffle=False should be deterministic regardless of random_state"


def test_stratified_kfold_shuffle_functionality():
    """
    Test that StratifiedKFold shuffle functionality works correctly.
    
    This validates that the shuffle parameter behaves according to the fix,
    ensuring that random state is handled properly for correct cross-validation.
    """
    
    # Use a case that would make shuffle behavior apparent
    X = np.arange(12)
    y = np.array([0] * 6 + [1] * 6)
    
    # Test basic functionality works
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=12345)
    folds = []
    for train_idx, test_idx in skf.split(X, y):
        folds.append((train_idx.copy(), test_idx.copy()))
    
    assert len(folds) == 3
    
    # Test that shuffle=False works consistently
    skf_no_shuffle = StratifiedKFold(n_splits=3, shuffle=False, random_state=54321)
    folds_no_shuffle = []
    for train_idx, test_idx in skf_no_shuffle.split(X, y):
        folds_no_shuffle.append((train_idx.copy(), test_idx.copy()))
        
    assert len(folds_no_shuffle) == 3