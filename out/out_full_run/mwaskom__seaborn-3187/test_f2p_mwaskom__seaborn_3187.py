"""Regression test for mwaskom/seaborn#3187

Ensure that numeric legend entries for large ranges do not lose their
multiplicative offset (i.e., the labels show the full numeric values
rather than scaled tick labels that rely on an external offset).
"""

import numpy as np
import matplotlib as mpl

from seaborn import utils


def test_locator_to_legend_entries_large_values():
    """Large numeric ranges should produce legend labels with full values.

    Before the fix, ScalarFormatter used an offset and the formatted
    tick strings were scaled (e.g., '1.04' for 1_040_000) which is
    incorrect for legends that don't show the offset. The expected
    behavior is that the returned string labels parse back to the
    original numeric levels.
    """
    locator = mpl.ticker.MaxNLocator(nbins=6)
    limits = (1_000_000.0, 1_400_000.0)

    levels, str_levels = utils.locator_to_legend_entries(locator, limits, float)

    # Parse the returned strings and compare numerically to the levels
    parsed = [float(s.replace(",", "")) for s in str_levels]
    assert np.allclose(parsed, levels)
