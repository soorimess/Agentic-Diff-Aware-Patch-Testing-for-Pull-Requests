"""
Regression test for KMeans n_jobs inconsistency bug.

This test ensures that KMeans with n_jobs=1 gives the same results as
n_jobs>1 when using the same random state.
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
    np.testing.assert_allclose(kmeans_1.inertia_, kmeans_2.inertia_, 
                              rtol=1e-10, atol=1e-10)
    
    # Also check that the cluster centers are identical
    np.testing.assert_allclose(kmeans_1.cluster_centers_, kmeans_2.cluster_centers_,
                              rtol=1e-10, atol=1e-10)
    
    # Test with n_jobs=4 as well
    kmeans_4 = KMeans(n_clusters=10, random_state=2, n_jobs=4)
    kmeans_4.fit(X)
    
    # All should give the same inertia
    np.testing.assert_allclose(kmeans_1.inertia_, kmeans_4.inertia_,
                              rtol=1e-10, atol=1e-10)
    
    # All should give the same cluster centers
    np.testing.assert_allclose(kmeans_1.cluster_centers_, kmeans_4.cluster_centers_,
                              rtol=1e-10, atol=1e-10)


def test_kmeans_n_init_consistency():
    """Test that KMeans with different n_init values also works consistently."""
    # Generate some data
    X, y = make_blobs(n_samples=1000, centers=5, n_features=2, random_state=42)
    
    # Run KMeans with different n_jobs and n_init values
    kmeans_1 = KMeans(n_clusters=5, random_state=2, n_jobs=1, n_init=5)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=5, random_state=2, n_jobs=2, n_init=5)
    kmeans_2.fit(X)
    
    # The results should be identical
    np.testing.assert_allclose(kmeans_1.inertia_, kmeans_2.inertia_,
                              rtol=1e-10, atol=1e-10)