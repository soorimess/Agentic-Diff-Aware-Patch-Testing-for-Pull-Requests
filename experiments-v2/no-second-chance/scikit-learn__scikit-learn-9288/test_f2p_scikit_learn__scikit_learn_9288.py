"""
Test to verify that KMeans gives consistent results for n_jobs=1 vs n_jobs>1.

This test ensures that KMeans clustering produces the same inertia value
regardless of whether n_jobs=1 or n_jobs>1 is used, which was a bug
where the single-threaded and multi-threaded versions gave slightly
different results due to different random number generation.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives exactly same results for n_jobs=1 and n_jobs>1."""
    # Generate some data exactly as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)

    # Run KMeans with different n_jobs values
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    
    # The inertia should be exactly the same for both cases
    # This assertion will fail in the buggy version but pass in the fixed version
    assert kmeans_1.inertia_ == kmeans_2.inertia_, (
        f"Inertia values differ: n_jobs=1: {kmeans_1.inertia_}, "
        f"n_jobs=2: {kmeans_2.inertia_}"
    )