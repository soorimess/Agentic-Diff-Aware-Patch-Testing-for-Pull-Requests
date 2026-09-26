"""
Test for regression of KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test ensures that KMeans with n_jobs=1 gives the same results as
n_jobs>1 when using the same random state, which was broken by a change
that made the behavior inconsistent.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that n_jobs=1 and n_jobs>1 give consistent results."""
    # Generate some data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up the same parameters for both cases
    params = {
        'n_clusters': 10,
        'random_state': 2,
        'n_init': 10
    }
    
    # Run KMeans with n_jobs=1
    kmeans_1 = KMeans(n_jobs=1, **params)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run KMeans with n_jobs=2 (or any > 1)
    kmeans_2 = KMeans(n_jobs=2, **params)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # They should be equal (or very close due to floating point precision)
    # Before the fix, they were different due to inconsistent random seed usage
    np.testing.assert_allclose(inertia_1, inertia_2, rtol=1e-10)


def test_kmeans_n_jobs_consistency_multiple_jobs():
    """Test that n_jobs=1 and various n_jobs values give consistent results."""
    # Generate some data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up the same parameters for all cases
    params = {
        'n_clusters': 10,
        'random_state': 2,
        'n_init': 10
    }
    
    # Run KMeans with n_jobs=1
    kmeans_1 = KMeans(n_jobs=1, **params)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run KMeans with n_jobs=3
    kmeans_3 = KMeans(n_jobs=3, **params)
    kmeans_3.fit(X)
    inertia_3 = kmeans_3.inertia_
    
    # Run KMeans with n_jobs=4
    kmeans_4 = KMeans(n_jobs=4, **params)
    kmeans_4.fit(X)
    inertia_4 = kmeans_4.inertia_
    
    # All should be equal (or very close due to floating point precision)
    np.testing.assert_allclose(inertia_1, inertia_3, rtol=1e-10)
    np.testing.assert_allclose(inertia_1, inertia_4, rtol=1e-10)