"""Test for KMeans n_jobs consistency bug fix.

This test verifies that KMeans gives consistent results regardless of
n_jobs parameter value, fixing the issue where n_jobs=1 gave different
results than n_jobs>1 due to inconsistent seeding.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same results for n_jobs=1 vs n_jobs>1."""
    # Generate test data as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with different n_jobs values using same parameters
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1, n_init=10)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2, n_init=10)
    
    kmeans_1.fit(X)
    kmeans_2.fit(X)
    
    # The bug would cause these to differ - they should be nearly identical
    inertia_1 = kmeans_1.inertia_
    inertia_2 = kmeans_2.inertia_
    
    # Should be very close, within a reasonable tolerance
    # This reflects the fact that both should use exactly the same random initialization approach
    assert np.isclose(inertia_1, inertia_2, rtol=1e-10), (
        f"Inertia values differ significantly: n_jobs=1={inertia_1}, n_jobs=2={inertia_2}. "
        "This indicates inconsistent seeding in KMeans."
    )


if __name__ == "__main__":
    test_kmeans_n_jobs_consistency()
    print("Test passed - KMeans n_jobs consistency verified!")