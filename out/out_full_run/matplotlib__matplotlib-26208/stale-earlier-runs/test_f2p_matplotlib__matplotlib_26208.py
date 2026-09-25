import numpy as np
import matplotlib

# Use non-interactive backend for tests
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def test_twinx_stackplot_preserves_ax1_datalim():
    """Regression test for issue where ax1.dataLim becomes infinite.

    This reproduces the sequence reported in the issue:
      - create ax1 and call stackplot on it
      - create ax2 = ax1.twinx()
      - plot on ax2

    Previously (before the fix) this sequence could replace ax1.dataLim with
    +/-inf.  The desired behaviour is that ax1.dataLim stays equal to the
    limits resulting from the stackplot.
    """
    x = ["16 May", "17 May"]
    y1 = [-22.717708333333402, 26.584999999999937]
    y2 = [-0.08501399999999998, -2.9833019999999966]

    fig, ax1 = plt.subplots()
    ax1.stackplot(x, y1)
    # capture the data limits after drawing on ax1 only
    before = np.array(ax1.dataLim.intervaly, dtype=float)

    ax2 = ax1.twinx()
    # plotting on the twin should not change ax1.dataLim
    ax2.plot(x, y2)

    after = np.array(ax1.dataLim.intervaly, dtype=float)

    # Ensure that ax1.dataLim did not become infinite
    assert np.all(np.isfinite(after)), "ax1.dataLim became infinite"

    # And that the limits are unchanged from before plotting on the twin
    np.testing.assert_allclose(after, before)
