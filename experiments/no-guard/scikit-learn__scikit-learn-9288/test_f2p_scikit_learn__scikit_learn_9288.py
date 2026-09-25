"""Regression test for KMeans n_jobs consistency bug.

This test ensures that KMeans gives consistent results regardless of
the number of jobs used when the same random_state is provided.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives the same result for n_jobs=1 vs n_jobs>1 with same random_state."""
    # Generate some data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with different n_jobs values
    results = {}
    for n_jobs in [1, 2, 3, 4]:
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
    
    # All results should be identical (within floating point precision)
    expected_inertia = results[1]
    for n_jobs in [2, 3, 4]:
        # Use a tolerance that's appropriate for the scale of the inertia
        assert np.isclose(results[n_jobs], expected_inertia, rtol=1e-10), (
            f"n_jobs={n_jobs} gives different inertia {results[n_jobs]} "
            f"than n_jobs=1 {expected_inertia}"
        )


def test_kmeans_n_jobs_centers_consistency():
    """Test that KMeans centers are the same for n_jobs=1 vs n_jobs>1 with same random_state."""
    # Generate some data
    X, y = make_blobs(n_samples=1000, centers=5, n_features=2, random_state=42)
    
    # Run KMeans with different n_jobs values
    results = {}
    for n_jobs in [1, 2, 3]:
        kmeans = KMeans(n_clusters=5, random_state=42, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.cluster_centers_
    
    # All center results should be identical
    expected_centers = results[1]
    for n_jobs in [2, 3]:
        assert np.allclose(results[n_jobs], expected_centers, rtol=1e-10), (
            f"n_jobs={n_jobs} gives different centers than n_jobs=1"
        )


def test_kmeans_n_jobs_labels_consistency():
    """Test that KMeans labels are the same for n_jobs=1 vs n_jobs>1 with same random_state."""
    # Generate some data
    X, y = make_blobs(n_samples=1000, centers=3, n_features=2, random_state=123)
    
    # Run KMeans with different n_jobs values
    results = {}
    for n_jobs in [1, 2, 3]:
        kmeans = KMeans(n_clusters=3, random_state=123, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.labels_
    
    # All label results should be identical  
    expected_labels = results[1]
    for n_jobs in [2, 3]:
        assert np.array_equal(results[n_jobs], expected_labels), (
            f"n_jobs={n_jobs} gives different labels than n_jobs=1"
        )