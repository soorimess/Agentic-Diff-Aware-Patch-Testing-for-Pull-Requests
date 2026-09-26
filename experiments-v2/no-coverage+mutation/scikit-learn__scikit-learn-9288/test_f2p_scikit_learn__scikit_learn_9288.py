"""
Test to verify that KMeans gives consistent results for n_jobs=1 vs n_jobs>1.

This test ensures that when using the same random_state, KMeans should give
identical results regardless of whether n_jobs=1 or n_jobs>1.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency_with_explicit_seed():
    """Test that KMeans gives same results for n_jobs=1 vs n_jobs>1 with explicit seed."""
    # Generate some data
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with n_jobs=1 using explicit seed
    kmeans_1 = KMeans(n_clusters=10, random_state=42, n_jobs=1, n_init=5)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    # Run KMeans with n_jobs=2 using same explicit seed
    kmeans_2 = KMeans(n_clusters=10, random_state=42, n_jobs=2, n_init=5)
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # The results should be identical (this is the core bug being tested)
    assert np.isclose(inertia_1, inertia_2), (
        f"Inertia mismatch: n_jobs=1={inertia_1}, n_jobs=2={inertia_2}"
    )


def test_kmeans_exact_bug_report_scenario():
    """Test the exact scenario from the bug report to show the inconsistency."""
    # Generate some data exactly as in bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)

    # Run KMeans with various n_jobs values exactly as in bug report
    results = {}
    for n_jobs in range(1, 5):
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
    
    # Before fix: n_jobs=1 would be different from n_jobs=2,3,4
    # After fix: they should all be the same
    # This test verifies the fix works
    assert np.isclose(results[1], results[2]), (
        f"Inertia mismatch: n_jobs=1={results[1]}, n_jobs=2={results[2]}"
    )
    assert np.isclose(results[1], results[3]), (
        f"Inertia mismatch: n_jobs=1={results[1]}, n_jobs=3={results[3]}"
    )
    assert np.isclose(results[1], results[4]), (
        f"Inertia mismatch: n_jobs=1={results[1]}, n_jobs=4={results[4]}"
    )