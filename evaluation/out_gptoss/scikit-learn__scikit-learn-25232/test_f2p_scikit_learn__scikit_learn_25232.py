import numpy as np
from sklearn.impute import IterativeImputer


def test_iterative_imputer_fill_value_numeric():
    """Test that IterativeImputer accepts a custom fill_value for constant strategy.

    The test should fail before the change (TypeError) and pass after the change.
    It also verifies that the custom fill_value is used by checking that the
    imputed values are not the default 0.
    """
    X = np.array([[np.nan, 1], [2, np.nan]])
    # Use a small number of iterations to keep the test fast.
    imputer = IterativeImputer(
        initial_strategy="constant",
        fill_value=5,
        max_iter=1,
        random_state=0,
    )
    X_imputed = imputer.fit_transform(X)
    # No missing values should remain.
    assert not np.isnan(X_imputed).any()
    # The imputed values should not be the default 0.
    assert (X_imputed != 0).all()
