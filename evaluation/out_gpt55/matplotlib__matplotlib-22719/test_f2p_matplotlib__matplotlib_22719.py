import logging
import warnings

import matplotlib.category as cat
from matplotlib._api import MatplotlibDeprecationWarning


def test_empty_category_data_is_not_treated_as_numeric_or_convertible(caplog):
    unit = cat.UnitData(["a", "b"])
    converter = cat.StrCategoryConverter()

    with warnings.catch_warnings():
        warnings.simplefilter("error", MatplotlibDeprecationWarning)
        converted = converter.convert([], unit, None)

    assert converted.shape == (0,)

    caplog.set_level(logging.INFO, logger="matplotlib.category")
    cat.UnitData().update([])

    assert not [
        record for record in caplog.records
        if record.name == "matplotlib.category"
        and "all parsable as floats or dates" in record.getMessage()
    ]
