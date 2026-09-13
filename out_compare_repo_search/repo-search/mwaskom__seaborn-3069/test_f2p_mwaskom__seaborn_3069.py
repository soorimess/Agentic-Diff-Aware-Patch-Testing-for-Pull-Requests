import matplotlib
matplotlib.use('Agg')

import contextlib
import pandas as pd

# Some pandas versions removed the 'mode.use_inf_as_null' option. The plotting
# machinery uses pd.option_context(...). If that option is missing the context
# manager raises an OptionError; override option_context to return a no-op
# context manager to allow the test to run across pandas versions.
pd.option_context = lambda *args, **kwargs: contextlib.nullcontext()

from seaborn._core.plot import Plot
from seaborn._core.scales import Nominal
from seaborn._marks.base import Mark


class SimpleMark(Mark):
    def _plot(self, split_gen, scales, orient):
        # Iterate the split generator so the plotting machinery runs,
        # but don't draw anything.
        for keys, data, ax in split_gen():
            pass

    def _legend_artist(self, variables, value, scales):
        return None


def test_nominal_scale_sets_categorical_limits_and_inverts_y():
    """
    Regression test for mwaskom/seaborn#3069:
    Nominal scales should be drawn like categorical scales:
      - x axis limits should be (-0.5, n_ticks - 0.5)
      - y axis limits should be inverted (n_ticks - 0.5, -0.5)
    """

    # X axis: nominal scale should get categorical padding
    p = Plot(x=["a", "b", "c"]).scale(x=Nominal()).add(SimpleMark()).plot()
    ax = p._figure.axes[0]
    x_axis = ax.xaxis
    n_xticks = len(x_axis.get_major_ticks())
    assert ax.get_xlim() == (-0.5, float(n_xticks) - 0.5)

    # Y axis: nominal scale should get categorical padding and be inverted
    p = Plot(y=["a", "b", "c"]).scale(y=Nominal()).add(SimpleMark()).plot()
    ax = p._figure.axes[0]
    y_axis = ax.yaxis
    n_yticks = len(y_axis.get_major_ticks())
    assert ax.get_ylim() == (float(n_yticks) - 0.5, -0.5)
