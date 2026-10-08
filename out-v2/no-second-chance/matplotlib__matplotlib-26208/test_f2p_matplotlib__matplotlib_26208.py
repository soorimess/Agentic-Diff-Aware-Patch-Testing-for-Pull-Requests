import matplotlib.pyplot as plt
import numpy as np


def test_no_infinite_datalim():
    """Regression test for twinx dataLim corruption bug."""
    fig, ax = plt.subplots()
    ax.stackplot(['a', 'b'], [1, 2])
    twin = ax.twinx()
    datalim = twin.dataLim.intervaly
    plt.close(fig)
    assert not np.any(np.isinf(datalim))