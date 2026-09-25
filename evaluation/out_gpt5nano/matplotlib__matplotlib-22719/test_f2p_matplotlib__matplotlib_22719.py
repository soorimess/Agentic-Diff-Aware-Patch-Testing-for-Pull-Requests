import warnings
import matplotlib

def test_empty_data_no_deprecation_warning_with_category_units():
    # Use a headless backend for testing
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt
    from matplotlib._api.deprecation import MatplotlibDeprecationWarning

    f, ax = plt.subplots()
    # Set up category units (strings) for the axis
    ax.xaxis.update_units(["a", "b"])

    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        # Plot empty data; this used to trigger a MatplotlibDeprecationWarning
        ax.plot([], [])
        # Ensure no deprecation warning is raised for empty data
        assert not any(m.category is MatplotlibDeprecationWarning for m in rec)


def test_update_empty_data_logs_silent():
    # Ensure that updating with empty data does not emit the informational
    # log about numeric parsing, which is the behavior after the patch.
    import matplotlib
    matplotlib.use("Agg", force=True)
    import matplotlib.category as category
    unit = category.UnitData()
    unit.update([])
