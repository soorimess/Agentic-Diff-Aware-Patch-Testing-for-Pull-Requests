"""
Test for regression of KMeans n_jobs=1 vs n_jobs>1 inconsistency.

This test ensures that KMeans with n_jobs=1 gives the same results as
n_jobs>1 when using the same random_state and n_init parameters.
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def test_kmeans_n_jobs_consistency_exact_bug_report():
    """Test using the exact example from the bug report to ensure it's fixed."""
    # Generate some data exactly as in the bug report
    X, y = make_blobs(n_samples=10000, centers=10, n_features=2, random_state=2)

    # Run KMeans with various n_jobs values exactly as in bug report
    results = {}
    for n_jobs in range(1, 5):
        kmeans = KMeans(n_clusters=10, random_state=2, n_jobs=n_jobs)
        kmeans.fit(X)
        results[n_jobs] = kmeans.inertia_
        print(f'(n_jobs={n_jobs}) kmeans.inertia_ = {kmeans.inertia_}')
    
    # Before the fix, n_jobs=1 would give: 17815.004991244623
    # After the fix, all should give: 17815.060435554242 (or very close)
    # The bug was that n_jobs=1 gave a different result than n_jobs>1
    
    # Check that all results are essentially the same (within floating point precision)
    # The key test: n_jobs=1 should NOT differ significantly from n_jobs>1
    base_inertia = results[1]  # The baseline from n_jobs=1
    
    # All other n_jobs should match n_jobs=1 (within tolerance)
    for n_jobs in [2, 3, 4]:
        # Use a very strict tolerance to catch any difference
        assert np.allclose(results[n_jobs], base_inertia, rtol=1e-10, atol=1e-10), (
            f"Inertia mismatch for n_jobs={n_jobs}: {results[n_jobs]} vs baseline {base_inertia}"
        )