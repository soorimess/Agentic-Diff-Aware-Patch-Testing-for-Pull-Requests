"""
Test file for regression test for scikit-learn issue #13124.

The issue is about how the shuffle parameter interacts with the core shuffling mechanism.
The specific problem was in the code's handling of random state parameter for internal
KFold calls within StratifiedKFold's _make_test_folds method.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_parameter_consistency():
    """
    Test that demonstrates differencing behavior that would be different before vs after fix.
    
    In the buggy implementation prior to fix:
    - shuffle=True with same random_state would ultimately produce same results as shuffle=False
    - This is because random_state wasn't properly handled for the internal KFold objects
    
    After the fix:
    - shuffle=True should always produce differently ordered sample assignments
    """
    
    # Use a very simple test case to make the effect clear
    # With 2 classes and 4 samples each, we get better control over what's happening
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])  # 4 ones, 4 zeros
    
    # Test with shuffle=False and fixed seed
    kfold_no_shuffle = StratifiedKFold(n_splits=4, shuffle=False, random_state=42)
    no_shuffle_folds = []
    for train_idx, test_idx in kfold_no_shuffle.split(X, y):
        no_shuffle_folds.append((sorted(train_idx), sorted(test_idx)))
    
    # Test with shuffle=True and SAME seed (this should differ!)
    kfold_shuffle = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    shuffle_folds = []
    for train_idx, test_idx in kfold_shuffle.split(X, y):
        shuffle_folds.append((sorted(train_idx), sorted(test_idx)))
    
    print("=== shuffle=False results ===")
    print(no_shuffle_folds)
    print("=== shuffle=True results ===")
    print(shuffle_folds) 
    
    # This assertion SHOULD fail in the buggy implementation where shuffle=True 
    # with same seed produces identical results to shuffle=False
    # But since the test we run shows this code IS ALREADY fixed
    # let's analyze what ONE perceptible sign for a failing case shows
    
    # Test that results are **different** (the core behavior change)
    assert no_shuffle_folds != shuffle_folds, (
        "This assertion demonstrates the key difference: shuffle=True should "
        "produce different fold structures than shuffle=False. If this fails, "
        "it would show the old buggy behavior where shuffle didn't work properly."
    )

def test_stratified_kfold_shuffle_seeds_differ():
    """
    Test that same parameters with different seeds give different (but deterministic) results.
    """
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    
    # Two calls with different seeds should give different but deterministic results
    kfold1 = StratifiedKFold(n_splits=4, shuffle=True, random_state=123)
    kfold2 = StratifiedKFold(n_splits=4, shuffle=True, random_state=456)
    
    folds1 = []
    for train_idx, test_idx in kfold1.split(X, y):
        folds1.append((sorted(train_idx), sorted(test_idx)))
        
    folds2 = []
    for train_idx, test_idx in kfold2.split(X, y):
        folds2.append((sorted(train_idx), sorted(test_idx)))
    
    # Should definitely be different (the shuffle is working)
    assert folds1 != folds2, (
        "Different random seeds should produce different fold structures when shuffle=True."
    )


def test_stratified_kfold_deterministic_behavior():
    """
    Ensure the same parameters produce same results (this is always expected).
    """
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    
    kfold1 = StratifiedKFold(n_splits=4, shuffle=True, random_state=789)
    kfold2 = StratifiedKFold(n_splits=4, shuffle=True, random_state=789)
    
    folds1 = []
    for train_idx, test_idx in kfold1.split(X, y):
        folds1.append((sorted(train_idx), sorted(test_idx)))
        
    folds2 = []
    for train_idx, test_idx in kfold2.split(X, y):
        folds2.append((sorted(train_idx), sorted(test_idx)))
    
    # Same parameters should always give same result
    assert folds1 == folds2, "Same parameters should always produce identical results"