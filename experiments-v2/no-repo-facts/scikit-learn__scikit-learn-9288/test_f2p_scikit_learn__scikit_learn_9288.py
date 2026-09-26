"""
Test for KMeans n_jobs=1 vs n_jobs>1 consistency bug.

This test reproduces the bug where KMeans gives slightly different results
for n_jobs=1 vs. n_jobs > 1 due to inconsistent random seed handling.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same results for n_jobs=1 and n_jobs>1."""
    # Generate some data exactly as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with various n_jobs values
    results = {}
    for n_jobs in range(1, 5):
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
        print(f'(n_jobs={n_jobs}) kmeans.inertia_ = {kmeans.inertia_}')
    
    # All results should be identical (within floating point precision)
    # The bug causes n_jobs=1 to be different from n_jobs>1
    for n_jobs in range(2, 5):
        assert np.allclose(results[1], results[n_jobs], rtol=1e-10), \
            f"Inertia differs between n_jobs=1 ({results[1]}) and n_jobs={n_jobs} ({results[n_jobs]})"


def test_kmeans_n_jobs_consistency_simple():
    """Simpler test focusing on the core issue."""
    # Use the exact same setup as the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run with n_jobs=1
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run with n_jobs=2 (or more)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # These should be identical
    assert np.allclose(inertia_1, inertia_2, rtol=1e-10), \
        f"Inertia differs between n_jobs=1 ({inertia_1}) and n_jobs=2 ({inertia_2})"


if __name__ == "__main__":
    test_kmeans_n_jobs_consistency()
    test_kmeans_n_jobs_consistency_simple()
    print("All tests passed!")