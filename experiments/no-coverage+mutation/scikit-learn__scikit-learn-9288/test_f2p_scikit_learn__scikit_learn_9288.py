"""
Regression test for KMeans n_jobs=1 vs n_jobs>1 behavior difference.

This test catches the bug where KMeans would give slightly different results 
depending on whether n_jobs=1 or n_jobs>1 was used due to differences in how 
random seeds were handled in the two code paths.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_inertia_consistency():
    """Test that KMeans gives consistent inertia values for n_jobs=1 vs n_jobs>1.
    
    This directly reproduces the case from the bug report that showed:
    (n_jobs=1) kmeans.inertia_ = 17815.004991244623
    (n_jobs=2) kmeans.inertia_ = 17815.060435554242
    """
    # Reproduce the exact scenario from the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Run KMeans with various n_jobs values
    kmeans_1 = KMeans(n_clusters=10, random_state=2, n_jobs=1, n_init=10)
    kmeans_1.fit(X)
    inertia_1 = kmeans_1.inertia_
    
    kmeans_2 = KMeans(n_clusters=10, random_state=2, n_jobs=2, n_init=10)  
    kmeans_2.fit(X)
    inertia_2 = kmeans_2.inertia_
    
    # The bug was that these would be different, but they should be the same
    # The tolerance needs to be small enough to catch the actual bug but 
    # large enough to avoid numerical precision issues
    np.testing.assert_almost_equal(inertia_1, inertia_2, decimal=10,
                                   err_msg="n_jobs=1 and n_jobs=2 gave different "
                                           "inertia values - this indicates the bug exists")


def test_kmeans_n_jobs_single_init_consistency():
    """Test consistency with n_init=1 to make the difference more obvious."""
    # Generate some data
    X, y = make_blobs(n_samples=1000, centers=5, n_features=2, random_state=2)
    
    # Run with n_init=1 for deterministic results
    kmeans_1 = KMeans(n_clusters=5, random_state=2, n_jobs=1, n_init=1)
    kmeans_1.fit(X)
    
    kmeans_2 = KMeans(n_clusters=5, random_state=2, n_jobs=2, n_init=1)
    kmeans_2.fit(X)
    
    # These should give exactly the same result 
    np.testing.assert_almost_equal(kmeans_1.inertia_, kmeans_2.inertia_, decimal=10,
                                   err_msg="n_jobs=1 and n_jobs=2 gave different "
                                           "inertia values with n_init=1")


def test_kmeans_multiple_n_jobs_consistency():
    """Test consistency across multiple job counts."""
    # Create same scenario as in the bug report but with one more detailed test  
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)
    
    # Test with multiple n_jobs configurations 
    results = {}
    for n_jobs in [1, 2, 3, 4]:
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs, n_init=10)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
        
    # All should give exactly the same result (if fix is in place)
    first_result = results[1]
    for n_jobs, inertia in results.items():
        np.testing.assert_almost_equal(inertia, first_result, decimal=10,
                                       err_msg=f"n_jobs={n_jobs} gave different "
                                               f"inertia compared to n_jobs=1")


if __name__ == "__main__":
    test_kmeans_n_jobs_inertia_consistency()
    test_kmeans_n_jobs_single_init_consistency() 
    test_kmeans_multiple_n_jobs_consistency()
    print("All tests passed!")