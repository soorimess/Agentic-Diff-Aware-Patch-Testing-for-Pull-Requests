import numpy as np
import matplotlib as mpl

from seaborn.utils import locator_to_legend_entries


def test_large_numeric_range_legend_labels_are_not_offset():
    """For large numeric ranges, legend labels should show full numbers.

    Previously, ScalarFormatter would use an offset (e.g. 1e6) and return
    scaled tick strings like '1.04' while omitting the multiplicative offset
    from the legend. The desired behavior is to have legend labels that
    represent the actual tick values (e.g., '1040000').
    """
    # Choose a locator and limits that will trigger offset/scientific formatting
    locator = mpl.ticker.MaxNLocator(nbins=3)
    limits = (1e6, 1.2e6)

    levels, str_levels = locator_to_legend_entries(locator, limits, float)

    # The formatted strings should parse back to the original numeric levels
    parsed = np.array([float(s) for s in str_levels])
    assert np.allclose(parsed, np.array(levels))
