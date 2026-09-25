"""Test for regression of KMeans n_jobs=1 vs n_jobs>1 consistency issue."""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """Test that KMeans gives same results for n_jobs=1 and n_jobs>1 with same random state.
    
    This test ensures that the change in behavior when n_jobs=1 behaves consistently
    with n_jobs>1 by using the same random seeds for both cases.
    """
    # Generate some test data as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with different n_jobs values using same random_state
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    
    # The results should be the same (or very close) due to same random_state
    # Before the fix, n_jobs=1 would use same random_state across iterations
    # while n_jobs>1 would use different seeds, causing inconsistency
    # After the fix, both should give consistent results
    assert np.allclose(kmeans_1.inertia_, kmeans_2.inertia_, rtol=1e-10), (
        f"Inertia mismatch: n_jobs=1={kmeans_1.inertia_} vs n_jobs=2={kmeans_2.inertia_}"
    )
    
    # Also test with more jobs to make sure consistency works across the board
    kmeans_3 = KMeans(n_clusters=10, random_state=2, n_jobs=3)
    kmeans_3.fit(X)
    
    kmeans_4 = KMeans(n_clusters=10, random_state=2, n_jobs=4)
    kmeans_4.fit(X)
    
    # All should give same results with same random_state
    assert np.allclose(kmeans_1.inertia_, kmeans_3.inertia_, rtol=1e-10), (
        f"Inertia mismatch: n_jobs=1={kmeans_1.inertia_} vs n_jobs=3={kmeans_3.inertia_}"
    )
    
    assert np.allclose(kmeans_1.inertia_, kmeans_4.inertia_, rtol=1e-10), (
        f"Inertia mismatch: n_jobs=1={kmeans_1.inertia_} vs n_jobs=4={kmeans_4.inertia_}"
    )