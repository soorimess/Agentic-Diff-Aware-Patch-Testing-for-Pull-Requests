"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test ensures that KMeans with n_jobs=1 produces the same results as
n_jobs>1 when using the same random_state and n_init parameters.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same results for n_jobs=1 vs n_jobs>1."""
    # Generate test data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up the same parameters for both cases
    random_state = 2
    n_clusters = 10
    n_init = 10
    
    # Run KMeans with n_jobs=1
    kmeans_1 = KMeans(n_clusters=n_clusters, random_state=random_state, 
                      n_jobs=1, n_init=n_init)
    kmeans_1.fit(X)
    
    # Run KMeans with n_jobs=2 (or more)
    kmeans_2 = KMeans(n_clusters=n_clusters, random_state=random_state, 
                      n_jobs=2, n_init=n_init)
    kmeans_2.fit(X)
    
    # The results should be identical
    assert np.allclose(kmeans_1.inertia_, kmeans_2.inertia_), (
        f"Inertia mismatch: {kmeans_1.inertia_} vs {kmeans_2.inertia_}"
    )
    
    # Also check that cluster centers are identical
    assert np.allclose(kmeans_1.cluster_centers_, kmeans_2.cluster_centers_), (
        "Cluster centers should be identical"
    )


def test_kmeans_n_jobs_consistency_multiple_jobs():
    """Test that KMeans gives same results for different n_jobs values."""
    # Generate test data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up the same parameters for all cases
    random_state = 2
    n_clusters = 10
    n_init = 10
    
    # Test with different n_jobs values
    results = {}
    for n_jobs in [1, 2, 3, 4]:
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, 
                       n_jobs=n_jobs, n_init=n_init)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
    
    # All results should be identical
    first_result = results[1]
    for n_jobs, inertia in results.items():
        assert np.allclose(first_result, inertia), (
            f"Inertia mismatch for n_jobs={n_jobs}: {first_result} vs {inertia}"
        )