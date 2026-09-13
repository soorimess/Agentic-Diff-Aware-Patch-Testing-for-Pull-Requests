import numpy as np
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose


def test_hist_respects_range_with_density():
    """Ensure hist(..., density=True) respects the ``range`` kwarg.

    Regression test for matplotlib#13989: when ``density=True`` the
    ``range`` kwarg was accidentally dropped for single-dataset calls,
    causing the returned bin edges to be computed from the data
    instead of the provided range.
    """
    x = np.linspace(0.1, 0.9, 10)
    # use 'auto' bins as in the original report
    _, bins, _ = plt.hist(x, bins='auto', range=(0, 1), density=True)
    # The bin edges must start at 0 and end at 1 when range=(0, 1) is given
    assert_allclose(bins[0], 0.0)
    assert_allclose(bins[-1], 1.0)
    plt.close('all')
