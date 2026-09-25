"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test verifies that KMeans with n_jobs=1 and n_jobs>1 give identical results
when initialized with the same random state, which is a regression from the fix
that makes the behavior consistent.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives identical results for n_jobs=1 vs n_jobs>1 with same random_state"""
    # Generate the same data as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Both runs with same parameters except n_jobs
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1, n_init=10)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2, n_init=10)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # With the fix, these should be identical (but currently fail due to bug)
    assert inertia_1 == inertia_2, (
        f"KMeans with n_jobs=1 and n_jobs=2 give different inertia values: "
        f"{inertia_1} vs {inertia_2} - this demonstrates the bug"
    )


def test_kmeans_n_jobs_consistency_multiple_jobs():
    """Test that KMeans gives identical results for all n_jobs values with same random_state"""
    # Generate the same data as in the bug report  
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run with n_jobs=1 (reference)
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1, n_init=10)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Test multiple different n_jobs values - all should match n_jobs=1
    for n_jobs in [2, 3, 4]:
        kmeans_n = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs, n_init=10)
        kmeans_n.fit(X)
        inertia_n = kmeans_n.inertia_
        
        # All should match the n_jobs=1 result
        assert inertia_1 == inertia_n, (
            f"KMeans with n_jobs=1 and n_jobs={n_jobs} give different inertia values: "
            f"{inertia_1} vs {inertia_n} - this demonstrates the bug"
        )