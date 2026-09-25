"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test ensures that KMeans produces identical results regardless of 
whether n_jobs=1 or n_jobs>1 is used, which was a bug in scikit-learn.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency():
    """
    Test that KMeans gives same results for n_jobs=1 vs n_jobs>1.
    
    Before the fix, this would fail due to different random seeds being used
    in the single-threaded vs multi-threaded code paths.
    """
    # Generate some data that would be sensitive to small differences
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with n_jobs=1
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run KMeans with n_jobs=2 (or any > 1)
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # They should be identical (within reasonable floating point tolerance)
    # This detects the inconsistent behavior where they were different due to seeds
    np.testing.assert_allclose(inertia_1, inertia_2, rtol=1e-10, atol=1e-10)


def test_kmeans_n_jobs_consistency_multiple_jobs():
    """
    Test that KMeans gives same results across different n_jobs values.
    
    This ensures consistency not just for n_jobs=1 vs n_jobs=2, but 
    also n_jobs=1 vs n_jobs=3, n_jobs=4, etc.
    """
    # Generate some data that would be sensitive to small differences 
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Test various n_jobs values, all should produce identical results
    results = {}
    for n_jobs in [1, 2, 3, 4]:
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
    
    # All results should be identical (within reasonable floating point tolerance)
    first_result = list(results.values())[0]
    for n_jobs, inertia in results.items():
        np.testing.assert_allclose(first_result, inertia, rtol=1e-10, atol=1e-10)


if __name__ == "__main__":
    # Run the tests if the file is executed directly
    test_kmeans_n_jobs_consistency()
    test_kmeans_n_jobs_consistency_multiple_jobs()
    print("All tests passed!")