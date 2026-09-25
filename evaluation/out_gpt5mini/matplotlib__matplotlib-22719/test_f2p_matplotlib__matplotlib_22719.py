import matplotlib.pyplot as plt
from matplotlib._api import MatplotlibDeprecationWarning


def test_no_deprecation_for_empty_data_with_category_units(recwarn):
    """Ensure plotting empty data on an axis with string/category units
    does not emit a MatplotlibDeprecationWarning.

    See: matplotlib#22719
    """
    fig, ax = plt.subplots()
    # register categorical units on the x-axis
    ax.xaxis.update_units(["a", "b"])

    # plotting empty data used to trigger a MatplotlibDeprecationWarning
    ax.plot([], [])

    # also exercise direct conversion path
    ax.convert_xunits([])

    # Assert that no MatplotlibDeprecationWarning was recorded.
    assert not any(
        issubclass(wi.category, MatplotlibDeprecationWarning) for wi in recwarn
    )
