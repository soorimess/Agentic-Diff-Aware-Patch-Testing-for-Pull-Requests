import numpy as np
import matplotlib as mpl
import pandas as pd

from seaborn.utils import locator_to_legend_entries
from seaborn._core.scales import Continuous
from seaborn._core.properties import IntervalProperty


def test_locator_to_legend_entries_preserves_absolute_values():
    """
    Regression test for mwaskom/seaborn#3187:
    Ensure that legend label formatting does not drop the ScalarFormatter offset
    (i.e., formatted legend entries should represent the absolute tick values,
    not only the offset part).
    """
    # Force use of offset behavior in the formatter to reproduce the problematic
    # state that existed before the fix.
    orig_useoffset = mpl.rcParams.get("axes.formatter.useoffset")
    try:
        mpl.rcParams["axes.formatter.useoffset"] = True

        locator = mpl.ticker.MaxNLocator(nbins=3)
        limits = (1_000_100, 1_000_900)

        levels, str_levels = locator_to_legend_entries(locator, limits, float)

        # Convert formatted strings back to numbers (tolerate thousands
        # separators if present) and assert they match the raw locator levels.
        parsed = [float(s.replace(",", "")) for s in str_levels]

        assert np.allclose(parsed, levels)

    finally:
        if orig_useoffset is None:
            try:
                del mpl.rcParams["axes.formatter.useoffset"]
            except Exception:
                pass
        else:
            mpl.rcParams["axes.formatter.useoffset"] = orig_useoffset


def test_continuous_setup_legend_formatter_preserves_absolute_values():
    """
    Also assert that the Continuous scale's legend generation does not rely on the
    ScalarFormatter offset (this exercises the code path in _core/scales.py).
    """
    orig_useoffset = mpl.rcParams.get("axes.formatter.useoffset")
    try:
        mpl.rcParams["axes.formatter.useoffset"] = True

        data = pd.Series([1_000_300.0, 1_000_600.0, 1_000_900.0], name="x")
        s = Continuous()._setup(data, IntervalProperty())

        assert s._legend is not None
        locs, labels = s._legend

        parsed = [float(lbl.replace(",", "")) for lbl in labels]
        assert np.allclose(parsed, locs)

    finally:
        if orig_useoffset is None:
            try:
                del mpl.rcParams["axes.formatter.useoffset"]
            except Exception:
                pass
        else:
            mpl.rcParams["axes.formatter.useoffset"] = orig_useoffset
