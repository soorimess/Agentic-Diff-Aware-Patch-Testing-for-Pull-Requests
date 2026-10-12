import numpy as np
from numpy.testing import assert_allclose

from scipy.signal import hilbert2


def test_hilbert2_accepts_nested_lists():
    x = [[1, 2, 3], [4, 5, 6]]
    assert_allclose(hilbert2(x), hilbert2(np.asarray(x, dtype=float)))
