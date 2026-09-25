import numpy as np

from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.utils._testing import assert_allclose


def test_iterative_imputer_constant_initialization_uses_fill_value():
    X = np.array([[np.nan, 10.0], [2.0, np.nan]])

    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=-5.0,
        max_iter=0,
    )

    assert_allclose(imputer.fit_transform(X), [[-5.0, 10.0], [2.0, -5.0]])
