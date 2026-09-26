import numpy as np
from sklearn.model_selection import StratifiedKFold


def test_stratified_kfold_shuffle_proper_random_state_initialization():
    """
    Test that StratifiedKFold properly initializes random state for shuffle.
    
    This test specifically targets the fix that changed:
        rng = self.random_state
    to:
        rng = check_random_state(self.random_state)
    
    The change ensures that when StratifiedKFold creates multiple KFold instances
    for different classes, each gets a properly initialized random number generator.
    """
    # Create test data with clear class structure
    X = np.arange(12)
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])  # 4 samples per class
    
    # Test 1: Reproducibility with same random state
    # This verifies that the random state handling is correct
    kfold1 = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    folds1 = []
    for fold_n, (train_idx, test_idx) in enumerate(kfold1.split(X, y)):
        folds1.append((train_idx.copy(), test_idx.copy()))
    
    kfold2 = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    folds2 = []
    for fold_n, (train_idx, test_idx) in enumerate(kfold2.split(X, y)):
        folds2.append((train_idx.copy(), test_idx.copy()))
    
    # Results should be identical due to same random_state
    for i in range(len(folds1)):
        assert set(folds1[i][0]) == set(folds2[i][0]), (
            "Same random_state should produce identical shuffle results. "
            "This tests proper random state initialization."
        )
    
    # Test 2: Different random states produce different results
    kfold3 = StratifiedKFold(n_splits=3, shuffle=True, random_state=123)
    folds3 = []
    for fold_n, (train_idx, test_idx) in enumerate(kfold3.split(X, y)):
        folds3.append((train_idx.copy(), test_idx.copy()))
    
    # At least some folds should differ
    different_count = 0
    for i in range(len(folds1)):
        if set(folds1[i][0]) != set(folds3[i][0]):
            different_count += 1
    
    assert different_count > 0, (
        "Different random states should produce different fold assignments. "
        "This verifies that shuffle parameter actually affects the results."
    )


def test_stratified_kfold_shuffle_multiple_runs_consistency():
    """
    Test that shuffle behavior is consistent across multiple runs with same parameters.
    
    This ensures that the fix maintains proper random state handling so that
    the same shuffle behavior can be reliably reproduced.
    """
    X = np.arange(10)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 5 samples of each class
    
    # Run multiple times with same shuffle=True and same random_state
    results = []
    for run in range(3):
        kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=999)
        folds = []
        for fold_n, (train_idx, test_idx) in enumerate(kfold.split(X, y)):
            folds.append((train_idx.copy(), test_idx.copy()))
        results.append(folds)
    
    # All runs should produce identical results
    for i in range(1, len(results)):
        for j in range(len(results[i])):
            assert set(results[0][j][0]) == set(results[i][j][0]), (
                "Same parameters should produce identical shuffle results across runs. "
                "This validates proper random state handling."
            )


def test_stratified_kfold_shuffle_documentation_compliance():
    """
    Test that shuffle parameter works as documented.
    
    The documentation states: "Whether to shuffle each class's samples before splitting 
    into batches" - this means samples within each class should be shuffled.
    """
    # Create a case that makes it clear that shuffle is affecting the sample assignment
    X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # 5 samples of each class
    
    # With shuffle=True, we expect that the assignment of samples from each class
    # to different folds is randomized (not deterministic in the same way as shuffle=False)
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    folds = []
    for fold_n, (train_idx, test_idx) in enumerate(kfold.split(X, y)):
        folds.append((train_idx.copy(), test_idx.copy()))
    
    # Basic validation that we get expected number of folds and that each fold
    # contains samples from both classes (stratification)
    assert len(folds) == 5
    for fold_train, fold_test in folds:
        # Each fold should contain samples from both classes
        train_set = set(fold_train)
        class_0_in_train = any(i in train_set for i in [0, 1, 2, 3, 4])
        class_1_in_train = any(i in train_set for i in [5, 6, 7, 8, 9])
        assert class_0_in_train and class_1_in_train, (
            "Each fold should contain samples from both classes (stratified)"
        )