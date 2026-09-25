from sklearn.experimental import enable_iterative_imputer
import numpy as np

from sklearn.impute import IterativeImputer, SimpleImputer


def test_iterative_imputer_constant_fill_value_used_in_initialization():
    # When initial_strategy is 'constant' and a concrete fill_value is provided,
    # the initial imputation should use that fill_value.
    X = np.array([[1.0], [np.nan], [3.0]], dtype=float)
    imp = IterativeImputer(initial_strategy="constant", fill_value=42.0, random_state=0)
    imp.fit(X)
    assert isinstance(imp.initial_imputer_, SimpleImputer)
    assert imp.initial_imputer_.fill_value == 42.0


def test_iterative_imputer_allows_nan_as_fill_value():
    # The API should allow np.nan as a fill_value when initial_strategy is 'constant'.
    X = np.array([[1.0], [np.nan], [3.0]], dtype=float)
    imp = IterativeImputer(initial_strategy="constant", fill_value=np.nan, random_state=0)
    imp.fit(X)
    assert isinstance(imp.initial_imputer_, SimpleImputer)
    assert np.isnan(imp.initial_imputer_.fill_value)


def test_param_validation_contains_fill_value_key():
    # Ensure there's a parameter-validation dictionary that includes a 'fill_value' key.
    import sklearn.impute._iterative as it
    dicts = [d for d in it.IterativeImputer.__dict__.values() if isinstance(d, dict)]
    assert any('fill_value' in d for d in dicts), (
        "No parameter-validation dictionary contains 'fill_value' key; "
        "this would miss catching certain mutation variants."
    )
