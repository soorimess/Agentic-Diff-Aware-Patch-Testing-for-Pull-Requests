import pandas as pd
import numpy as np

import matplotlib as mpl

from seaborn._core.plot import Plot
from seaborn._marks.base import Mark
from seaborn import rcmod


class EmptyMark(Mark):
    def _plot(self, split_gen, scales, orient):
        # Intentionally do nothing (don't iterate split_gen) to avoid
        # pandas option_context being entered on older pandas versions.
        return


def test_nominal_scale_grid_and_limits():
    """
    Nominal (categorical) scales should:
      - disable the axis grid even when the theme would show it
      - set axis limits to -0.5 .. (n_ticks - 0.5)
      - if on the y-axis, invert the axis so limits are (n_ticks - 0.5, -0.5)

    This reproduces the behavior introduced in mwaskom/seaborn PR: nominal
    scales are drawn like categorical axes.
    """

    df_x = pd.DataFrame({"cat": list("abc"), "y": [1, 2, 3]})
    df_y = pd.DataFrame({"x": [1, 2, 3], "cat": list("abc")})

    # Use a style that normally shows grid lines so we can detect the change
    with rcmod.axes_style("darkgrid"):
        p_x = Plot(df_x, x="cat", y="y").add(EmptyMark()).plot()
        p_y = Plot(df_y, x="x", y="cat").add(EmptyMark()).plot()

    ax_x = p_x._figure.axes[0]
    ax_y = p_y._figure.axes[0]

    # The gridlines along the categorical axes should be turned off
    x_grid_lines = ax_x.get_xgridlines()
    y_grid_lines = ax_y.get_ygridlines()
    # There may be zero or more grid line artists; if present they should be invisible
    assert all(not line.get_visible() for line in x_grid_lines)
    assert all(not line.get_visible() for line in y_grid_lines)

    # The x-axis limits should be exactly [-0.5, n_ticks - 0.5]
    nticks_x = len(ax_x.xaxis.get_major_ticks())
    assert ax_x.get_xlim() == (-0.5, nticks_x - 0.5)

    # The y-axis limits should be inverted: [n_ticks - 0.5, -0.5]
    nticks_y = len(ax_y.yaxis.get_major_ticks())
    assert ax_y.get_ylim() == (nticks_y - 0.5, -0.5)
