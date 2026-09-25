import matplotlib.pyplot as plt

from seaborn._core.plot import Plot


def test_nominal_scale_drawn_like_categorical():
    """
    Nominal scales should behave like categorical axes: limits set to
    +/- 0.5 from first/last tick, the grid turned off, and the y-axis
    inverted for vertical categorical axes.
    """

    # X axis (horizontal) should get limits (-0.5, n - 0.5) and grid off
    p = Plot(x=["a", "b", "c"]).plot()
    ax = p._figure.axes[0]
    assert ax.get_xlim() == (-0.5, 2.5)
    assert all(not g.get_visible() for g in ax.xaxis.get_gridlines())

    plt.close(p._figure)

    # Y axis (vertical) should get limits (n - 0.5, -0.5) and grid off
    p = Plot(y=["a", "b", "c"]).plot()
    ax = p._figure.axes[0]
    assert ax.get_ylim() == (2.5, -0.5)
    assert all(not g.get_visible() for g in ax.yaxis.get_gridlines())

    plt.close(p._figure)
