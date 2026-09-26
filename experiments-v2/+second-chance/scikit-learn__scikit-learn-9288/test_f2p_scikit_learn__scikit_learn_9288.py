"""
Test for KMeans n_jobs consistency bug.

This test ensures that KMeans with n_jobs=1 gives the same results as
n_jobs>1 when using the same random state and data.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same results for n_jobs=1 vs n_jobs>1."""
    # Generate some data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with different n_jobs values
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    
    # The results should be identical
    assert np.allclose(kmeans_1.inertia_, kmeans_2.inertia_), (
        f"Inertia differs: {kmeans_1.inertia_} vs {kmeans_2.inertia_}"
    )
    
    # Also test with n_jobs=4
    kmeans_4 = KMeans(n_clusters=10, random_state=2, n_jobs=4)
    kmeans_4.fit(X)
    
    assert np.allclose(kmeans_1.inertia_, kmeans_4.inertia_), (
        f"Inertia differs: {kmeans_1.inertia_} vs {kmeans_4.inertia_}"
    )
    
    # Test that the cluster centers are also the same
    assert np.allclose(kmeans_1.cluster_centers_, kmeans_2.cluster_centers_), (
        "Cluster centers differ between n_jobs=1 and n_jobs=2"
    )
    
    assert np.allclose(kmeans_1.cluster_centers_, kmeans_4.cluster_centers_), (
        "Cluster centers differ between n_jobs=1 and n_jobs=4"
    )


def test_kmeans_n_jobs_consistency_with_different_random_states():
    """Test that KMeans with same random_state but different n_jobs gives same results."""
    # Generate some data
    X, y = make_blobs(n_samples=5000, centers=5, n_features=3, random_state=42)
    
    # Run KMeans with different n_jobs values
    kmeans_1 = KMeans(n_clusters=5, random_state=42, n_jobs=1, n_init=5)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=5, random_state=42, n_jobs=3, n_init=5)
    kmeans_2.fit(X)
    
    # The results should be identical
    assert np.allclose(kmeans_1.inertia_, kmeans_2.inertia_), (
        f"Inertia differs: {kmeans_1.inertia_} vs {kmeans_2.inertia_}"
    )