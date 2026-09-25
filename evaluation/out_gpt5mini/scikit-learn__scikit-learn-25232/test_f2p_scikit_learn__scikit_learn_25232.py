import numpy as np
import pytest

from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer


def test_iterative_imputer_accepts_fill_value_and_uses_it_for_initial_constant_strategy():
    """Regression test for issue #25232.

    IterativeImputer should accept the parameter `fill_value` and pass it to
    the underlying SimpleImputer used for the initial imputation when
    `initial_strategy="constant"`.

    Before the fix, IterativeImputer did not accept `fill_value` and
    constructing it with that parameter raised TypeError. After the fix,
    the parameter is accepted and the initial_imputer_.statistics_ reflect
    the provided fill value.
    """
    X = np.array([[np.nan, 1.0], [4.0, 2.0], [5.0, 3.0]])

    # This would raise TypeError on the old (pre-fix) code because
    # IterativeImputer did not accept `fill_value`.
    imp = IterativeImputer(initial_strategy="constant", fill_value=123, random_state=0)

    # fit to trigger the creation of the internal SimpleImputer
    imp.fit(X)

    # The underlying SimpleImputer.statistics_ should contain the provided
    # fill_value for constant strategy (per-column).
    assert imp.initial_imputer_.statistics_.shape[0] == X.shape[1]
    assert np.allclose(imp.initial_imputer_.statistics_, 123)
