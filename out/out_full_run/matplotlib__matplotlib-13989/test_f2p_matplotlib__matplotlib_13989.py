import numpy as np
import matplotlib.pyplot as plt


def test_hist_respects_range_with_density():
    """Ensure hist(..., range=..., density=True) uses the provided range.

    This tests the regression where setting density=True accidentally
    dropped previously-set hist kwargs (notably 'range'), so the
    underlying numpy.histogram was called without the user-provided
    range and returned bin edges based on the data instead.
    """
    rng = np.random.RandomState(0)
    data = rng.rand(10)

    fig, ax = plt.subplots()
    try:
        _, bins, _ = ax.hist(data, bins='auto', range=(0, 1), density=True)
    finally:
        plt.close(fig)

    # The first and last bin edges must equal the requested range
    assert np.allclose([bins[0], bins[-1]], [0.0, 1.0])
