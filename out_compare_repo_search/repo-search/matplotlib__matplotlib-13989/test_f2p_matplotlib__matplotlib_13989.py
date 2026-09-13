import numpy as np
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose


def test_hist_respects_range_with_density():
    """Ensure that hist(..., range=..., density=True) respects the given range.

    Prior to the fix for #13989, passing density=True caused internal
    histogram kwargs to be overwritten and the provided `range` to be lost
    for single-dataset calls. This made the returned bin edges not match
    the requested range.
    """
    rng = np.random.RandomState(0)
    x = rng.rand(10)

    # use a single dataset, bins='auto', and an explicit range -- with the
    # bug this would be ignored when density=True and the returned bin
    # edges would not span the requested range.
    _, bins, _ = plt.hist(x, bins='auto', range=(0, 1), density=True)

    # The first and last bin edges must match the requested range exactly
    # (or within floating point tolerance).
    assert_allclose(bins[0], 0.0)
    assert_allclose(bins[-1], 1.0)

    plt.close('all')
