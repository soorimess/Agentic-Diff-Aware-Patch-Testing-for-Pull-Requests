"""
Test for KMeans n_jobs=1 vs n_jobs>1 consistency issue.

This test verifies that KMeans with n_jobs=1 and n_jobs>1 produce
consistent results when using the same random state, which was broken
by a change in how random seeds are handled in the k_means function.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """
    Test that KMeans gives same result for n_jobs=1 vs n_jobs>1 with same random_state.
    
    This test catches the bug where n_jobs=1 and n_jobs>1 would give different
    results due to inconsistent random seed handling.
    """
    # Use the exact same parameters as in the bug report to reproduce the issue
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Test with n_jobs=1
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Test with n_jobs=2 (or any > 1)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # The bug was that these would be different due to inconsistent seeding
    # After the fix, they should be the same
    assert np.isclose(inertia_1, inertia_2, rtol=1e-10), (
        f"Inertia differs between n_jobs=1 ({inertia_1}) and n_jobs=2 ({inertia_2}). "
        "This indicates inconsistent random seed handling in KMeans."
    )