"""
Test for regression of KMeans giving different result for n_jobs=1 vs n_jobs > 1.

Issue: KMeans gives slightly different result for n_jobs=1 vs. n_jobs > 1
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same result for n_jobs=1 and n_jobs > 1."""
    # Generate test data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Set up same parameters for all tests
    kwargs = {
        'n_clusters': 10,
        'random_state': 2,
        'max_iter': 100
    }
    
    # Run KMeans with n_jobs=1
    kmeans_1 = KMeans(n_jobs=1, **kwargs)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run KMeans with n_jobs=2 (or more)
    kmeans_n = KMeans(n_jobs=2, **kwargs)
    kmeans_n.fit(X)
    inertia_n = kmeans_n.inertia_
    
    # The results should be identical (within floating point precision)
    assert np.allclose(inertia_1, inertia_n, rtol=1e-10), (
        f"Inertia mismatch: n_jobs=1 gives {inertia_1}, n_jobs=2 gives {inertia_n}"
    )


def test_kmeans_n_jobs_multiple_seeds():
    """
    Test that KMeans with different n_jobs values produces consistent results
    even with multiple initializations (n_init parameter).
    """
    # Generate test data
    X, y = make_blobs(n_samples=5000, centers=5, n_features=3, random_state=42)
    
    # Test with different values of n_init
    for n_init in [1, 5, 10]:
        # Run with n_jobs=1
        kmeans_1 = KMeans(n_jobs=1, n_clusters=5, random_state=42, 
                         n_init=n_init, max_iter=100)
        kmeans_1.fit(X)
        inertia_1 = kmeans_1.inertia_
        
        # Run with n_jobs=3
        kmeans_n = KMeans(n_jobs=3, n_clusters=5, random_state=42,
                         n_init=n_init, max_iter=100)
        kmeans_n.fit(X)
        inertia_n = kmeans_n.inertia_
        
        # The results should be identical
        assert np.allclose(inertia_1, inertia_n, rtol=1e-10), (
            f"Inertia mismatch with n_init={n_init}: "
            f"n_jobs=1 gives {inertia_1}, n_jobs=3 gives {inertia_n}"
        )