"""
Regression test for KMeans n_jobs=1 vs n_jobs > 1 behavior difference

This test ensures that KMeans produces consistent results regardless of whether 
n_jobs=1 or n_jobs>1 is used, by testing that they produce the same inertia 
when given the same random_state.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_inertia_consistency():
    """Test that n_jobs=1 and n_jobs>1 give identical inertia values."""
    # Generate test data - using the exact same setup as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with different n_jobs values using same random_state
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2) 
    
    # Fit both models
    kmeans_1.fit(X)
    kmeans_2.fit(X)
    
    # They should produce identical inertia values (this was the bug)
    assert np.isclose(kmeans_1.inertia_, kmeans_2.inertia_), (
        f"Inertia mismatch: n_jobs=1={kmeans_1.inertia_}, n_jobs=2={kmeans_2.inertia_}. "
        "KMeans should produce consistent results regardless of n_jobs setting."
    )


def test_kmeans_multiple_n_jobs_inertia_consistency():
    """Test that all n_jobs values give identical results when using same random_state."""
    # Generate test data using exact parameters from bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Test various n_jobs values with same random_state - ensure consistency
    results = {}
    for n_jobs in range(1, 5):
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
        
    # All n_jobs values should give the same result (they are now consistent)
    first_inertia = results[1] 
    for n_jobs, inertia in results.items():
        assert np.isclose(first_inertia, inertia), (
            f"Inertia mismatch for n_jobs={n_jobs}: {inertia} vs {first_inertia}. "
            "All n_jobs values should give identical results with same random_state."
        )