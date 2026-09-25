import pytest

import numpy as np

from sklearn._config import config_context
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_union


def test_feature_union_with_pandas_transform_output_and_aggregating_transformer():
    """Regression test for scikit-learn#25747.

    FeatureUnion used with global pandas transform output should not attempt to
    set the index of a transformer's already-constructed DataFrame to the
    original input index. Some transformers may return aggregated
    DataFrames/Series (different length than the input); forcing the original
    index on such outputs raised a pandas ValueError before the fix.

    The test ensures that when the global configuration requests pandas output
    the FeatureUnion with a transformer that performs aggregation does not
    raise and returns a pandas-like object with the expected shape.
    """
    pd = pytest.importorskip("pandas")

    # Create a small timeseries-like DataFrame with repeated dates so that a
    # groupby aggregation reduces the number of rows.
    index = pd.date_range(start="2020-01-01", periods=10, freq="H")
    X = pd.DataFrame({"value": [1] * len(index)}, index=index)
    X["date"] = X.index.date

    class MyTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None, **kwargs):
            return self

        def transform(self, X):
            # Aggregates by date -> fewer rows than the original input
            return X.groupby(X["date"]).sum()

        def get_feature_names_out(self, input_features=None):
            # Return a single column name for the aggregated output
            return np.asarray(["value"], dtype=object)

    # Request pandas outputs globally for transform/fit_transform.
    with config_context(transform_output="pandas"):
        fu = make_union(MyTransformer())

        # Before the fix this call raised a pandas ValueError when trying to
        # assign the original (longer) index to the aggregated DataFrame. The
        # correct behaviour is to *not* override the index of an already
        # constructed DataFrame, so no exception should be raised and the
        # resulting object should be a pandas container with the aggregated
        # number of rows.
        result = fu.fit_transform(X)

    # Sanity-check the result is pandas-like and has the expected shape.
    assert hasattr(result, "iloc")
    # One column after aggregation (value), number of rows == number of unique dates
    assert result.shape[1] == 1
    assert result.shape[0] == X["date"].nunique()
