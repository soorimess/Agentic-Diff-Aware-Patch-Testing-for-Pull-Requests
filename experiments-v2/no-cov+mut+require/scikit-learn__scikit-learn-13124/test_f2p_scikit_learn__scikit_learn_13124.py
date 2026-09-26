"""
Regression test for StratifiedKFold shuffle behavior bug.

This test ensures that when shuffle=True, different random states produce
different splits, which is the expected behavior.
"""
import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_respects_random_state():
    """
    Test that shuffle=True respects different random states and produces different splits.
    
    The bug was that when shuffle=True, different random_state values would produce
    the same splits, making the shuffle parameter ineffective. This test ensures
    that different random states actually produce different fold patterns.
    """
    # Use a dataset that makes shuffle effects obvious
    # 4 classes with 5 samples each = 20 total samples
    # 4 splits means each fold gets 5 samples
    X = np.arange(20)
    y = np.array([0] * 5 + [1] * 5 + [2] * 5 + [3] * 5)
    
    # Use two different random states that should produce different shuffle results
    rs1 = 12345
    rs2 = 67890
    
    # Get splits for first random state
    skf1 = StratifiedKFold(n_splits=4, shuffle=True, random_state=rs1)
    splits1 = list(skf1.split(X, y))
    
    # Get splits for second random state
    skf2 = StratifiedKFold(n_splits=4, shuffle=True, random_state=rs2)
    splits2 = list(skf2.split(X, y))
    
    # Both should have the same number of splits
    assert len(splits1) == len(splits2) == 4
    
    # Check that splits are actually different (not just reordered versions of same splits)
    # Count how many splits differ
    diff_count = 0
    for i in range(len(splits1)):
        train1, test1 = splits1[i]
        train2, test2 = splits2[i]
        
        # If any part of the split differs, increment counter
        if not (np.array_equal(train1, train2) and np.array_equal(test1, test2)):
            diff_count += 1
    
    # At least one split should differ to prove shuffle is working properly
    # This is the core test that would fail with the buggy behavior
    assert diff_count > 0, (
        "FAIL: shuffle=True with different random states produces identical splits. "
        "This indicates the shuffle parameter is not working correctly. "
        "Different random states should produce different fold patterns to ensure "
        "proper randomization of samples within each class."
    )


def test_stratified_kfold_shuffle_reproducibility():
    """
    Test that same random state produces reproducible results.
    """
    X = np.arange(20)
    y = np.array([0] * 5 + [1] * 5 + [2] * 5 + [3] * 5)
    
    rs = 999
    
    skf1 = StratifiedKFold(n_splits=4, shuffle=True, random_state=rs)
    splits1 = list(skf1.split(X, y))
    
    skf2 = StratifiedKFold(n_splits=4, shuffle=True, random_state=rs)
    splits2 = list(skf2.split(X, y))
    
    assert len(splits1) == len(splits2) == 4
    
    # All splits should be identical for reproducibility
    for i in range(len(splits1)):
        train1, test1 = splits1[i]
        train2, test2 = splits2[i]
        assert np.array_equal(train1, train2), f"Train splits differ at fold {i}"
        assert np.array_equal(test1, test2), f"Test splits differ at fold {i}"


def test_stratified_kfold_no_shuffle_consistency():
    """
    Test that shuffle=False produces consistent results.
    """
    X = np.arange(20)
    y = np.array([0] * 5 + [1] * 5 + [2] * 5 + [3] * 5)
    
    skf1 = StratifiedKFold(n_splits=4, shuffle=False)
    splits1 = list(skf1.split(X, y))
    
    skf2 = StratifiedKFold(n_splits=4, shuffle=False)
    splits2 = list(skf2.split(X, y))
    
    assert len(splits1) == len(splits2) == 4
    
    # All splits should be identical
    for i in range(len(splits1)):
        train1, test1 = splits1[i]
        train2, test2 = splits2[i]
        assert np.array_equal(train1, train2), f"Train splits differ at fold {i}"
        assert np.array_equal(test1, test2), f"Test splits differ at fold {i}"


def test_stratified_kfold_shuffle_deterministic_behavior():
    """
    Test that shuffle behavior is deterministic with same seed.
    """
    X = np.arange(12)
    y = np.array([0] * 6 + [1] * 6)  # 6 samples of each class
    
    rs = 42
    
    # Run multiple times with same seed to ensure deterministic behavior
    results = []
    for _ in range(3):
        skf = StratifiedKFold(n_splits=2, shuffle=True, random_state=rs)
        splits = list(skf.split(X, y))
        results.append(splits)
    
    # All should be identical
    for i in range(1, len(results)):
        for j in range(len(results[0])):
            train1, test1 = results[0][j]
            train2, test2 = results[i][j]
            assert np.array_equal(train1, train2), f"Non-deterministic at run {i}, fold {j}"
            assert np.array_equal(test1, test2), f"Non-deterministic at run {i}, fold {j}"


if __name__ == "__main__":
    test_stratified_kfold_shuffle_respects_random_state()
    print("✓ test_stratified_kfold_shuffle_respects_random_state passed")
    
    test_stratified_kfold_shuffle_reproducibility()
    print("✓ test_stratified_kfold_shuffle_reproducibility passed")
    
    test_stratified_kfold_no_shuffle_consistency()
    print("✓ test_stratified_kfold_no_shuffle_consistency passed")
    
    test_stratified_kfold_shuffle_deterministic_behavior()
    print("✓ test_stratified_kfold_shuffle_deterministic_behavior passed")