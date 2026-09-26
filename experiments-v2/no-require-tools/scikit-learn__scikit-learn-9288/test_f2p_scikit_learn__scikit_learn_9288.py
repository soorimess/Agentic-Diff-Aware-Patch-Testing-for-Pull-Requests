"""
Test for KMeans n_jobs inconsistency bug.

This test ensures that KMeans with n_jobs=1 gives the same results as 
n_jobs>1 when using the same random state and data.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_inertia_consistency():
    """Test that n_jobs=1 and n_jobs>1 give identical inertia values."""
    # Generate the exact same data as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with various n_jobs values using same random_state
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    
    kmeans_3 = KMeans(n_clusters=10, random_state=2, n_jobs=3)
    kmeans_3.fit(X)
    
    kmeans_4 = KMeans(n_clusters=10, random_state=2, n_jobs=4)
    kmeans_4.fit(X)
    
    # Before the fix, n_jobs=1 would give different inertia than n_jobs>1
    # After the fix, they should all be the same
    expected_inertia = kmeans_2.inertia_  # Using n_jobs=2 as reference
    
    # Check that all results are consistent
    assert np.isclose(kmeans_1.inertia_, expected_inertia, rtol=1e-10), (
        f"n_jobs=1 inertia {kmeans_1.inertia_} differs from n_jobs=2 inertia {expected_inertia}"
    )
    assert np.isclose(kmeans_2.inertia_, expected_inertia, rtol=1e-10), (
        f"n_jobs=2 inertia {kmeans_2.inertia_} differs from reference {expected_inertia}"
    )
    assert np.isclose(kmeans_3.inertia_, expected_inertia, rtol=1e-10), (
        f"n_jobs=3 inertia {kmeans_3.inertia_} differs from reference {expected_inertia}"
    )
    assert np.isclose(kmeans_4.inertia_, expected_inertia, rtol=1e-10), (
        f"n_jobs=4 inertia {kmeans_4.inertia_} differs from reference {expected_inertia}"
    )


def test_kmeans_specific_bug_case():
    """Test the exact case reported in the bug."""
    # This reproduces the exact case from the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2)
    kmeans_2.fit(X)
    
    # The bug was that these were different
    # Before fix: kmeans_1.inertia_ = 17815.004991244623, kmeans_2.inertia_ = 17815.060435554242
    # After fix: they should be the same (or very close)
    
    # The tolerance needs to be tight enough to catch the bug but not too tight to be flaky
    assert np.isclose(kmeans_1.inertia_, kmeans_2.inertia_, rtol=1e-10), (
        f"Bug reproduced: n_jobs=1 inertia {kmeans_1.inertia_} != n_jobs=2 inertia {kmeans_2.inertia_}"
    )