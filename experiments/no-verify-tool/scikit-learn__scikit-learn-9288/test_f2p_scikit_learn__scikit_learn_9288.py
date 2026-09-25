"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test ensures that KMeans with n_jobs=1 gives the same results as
n_jobs>1 when using the same random state. This was broken by a change
that made the single-threaded case not use seeds.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans with n_jobs=1 gives same results as n_jobs>1."""
    # Generate test data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up identical parameters for both cases
    kwargs = {'n_clusters': 10, 'random_state': 2, 'n_init': 10, 'max_iter': 300}
    
    # Test with n_jobs=1
    kmeans_1 = KMeans(n_jobs=1, **kwargs)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Test with n_jobs=2 (or any > 1)
    kmeans_2 = KMeans(n_jobs=2, **kwargs)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # The results should be identical (or at least very close)
    # Before the fix, they were different due to different random seeds
    assert abs(inertia_1 - inertia_2) < 1e-10, (
        f"Inertia difference too large: {inertia_1} vs {inertia_2}"
    )


def test_kmeans_multiple_n_jobs_consistency():
    """Test that multiple n_jobs values give consistent results."""
    # Generate test data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Test different n_jobs values with same random state
    kwargs = {'n_clusters': 10, 'random_state': 2, 'n_init': 10, 'max_iter': 300}
    
    inertias = []
    for n_jobs in [1, 2, 3, 4]:
        kmeans = KMeans(n_jobs=n_jobs, **kwargs)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    # All results should be very close to each other
    first_inertia = inertias[0]
    for i, inertia in enumerate(inertias):
        assert abs(inertia - first_inertia) < 1e-10, (
            f"Inertia mismatch at n_jobs={i+1}: {inertia} vs {first_inertia}"
        )


if __name__ == "__main__":
    test_kmeans_n_jobs_consistency()
    test_kmeans_multiple_n_jobs_consistency()
    print("All tests passed!")