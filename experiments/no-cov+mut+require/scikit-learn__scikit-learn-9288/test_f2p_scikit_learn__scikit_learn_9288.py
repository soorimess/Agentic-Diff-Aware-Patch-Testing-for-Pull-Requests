"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test verifies that KMeans with n_jobs=1 and n_jobs>1 produce consistent 
results, which was broken before a fix was applied.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans produces consistent results for n_jobs=1 vs n_jobs>1."""
    # Test data from bug report 
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run with n_jobs=1 (before fix, this would be inconsistent with n_jobs>1)  
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1, n_init=10)
    kmeans_1.fit(X)
    
    # Run with n_jobs=2 (parallel case)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2, n_init=10) 
    kmeans_2.fit(X)
    
    # After fix: should be very close (within machine precision)
    # Before fix: would have significant difference (~0.055 based on bug report)
    inertia_diff = abs(kmeans_1.inertia_ - kmeans_2.inertia_)
    
    # With the fix applied, this difference should be tiny
    # Let's assert it's within reasonable floating point precision
    assert inertia_diff < 1e-8, (
        f"Significant difference between n_jobs=1 and n_jobs=2: {inertia_diff}\n"
        f"n_jobs=1: {kmeans_1.inertia_}\n"
        f"n_jobs=2: {kmeans_2.inertia_}"
    )