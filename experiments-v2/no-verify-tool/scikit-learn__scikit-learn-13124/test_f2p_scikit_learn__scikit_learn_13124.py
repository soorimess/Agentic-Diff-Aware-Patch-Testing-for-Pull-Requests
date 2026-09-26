"""
Test for StratifiedKFold shuffle behavior bug.

This test verifies that shuffle=True with different random states produces
different results, which was the bug reported in the issue.
"""

import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_shuffle_behavior():
    """
    Core test: shuffle=True should produce different splits with different random states.
    """
    # Simple test case
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    
    # Create two kfold objects with different random states
    kfold1 = StratifiedKFold(n_splits=2, shuffle=True, random_state=123)
    kfold2 = StratifiedKFold(n_splits=2, shuffle=True, random_state=456)
    
    splits1 = list(kfold1.split(X, y))
    splits2 = list(kfold2.split(X, y))
    
    # Both should produce valid splits
    assert len(splits1) == 2
    assert len(splits2) == 2
    
    # The key: different random states should produce different splits
    # This is the bug that was reported and fixed
    different = False
    for i in range(len(splits1)):
        train1, test1 = splits1[i]
        train2, test2 = splits2[i]
        if not (np.array_equal(train1, train2) and np.array_equal(test1, test2)):
            different = True
            break
    
    # This assertion will fail if shuffle parameter is broken
    assert different, (
        "BUG: shuffle=True with different random states produced identical splits. "
        "The shuffle parameter was not working correctly."
    )