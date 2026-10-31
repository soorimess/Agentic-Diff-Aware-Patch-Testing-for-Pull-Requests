"""
Regression test for the set_xindex and drop_indexes methods.
"""

from xarray import DataArray, Dataset


def test_set_xindex_exists():
    """Test that DataArray.set_xindex method exists."""
    da = DataArray([1, 2, 3], coords={'x': [0, 1, 2]}, dims='x')
    assert hasattr(da, 'set_xindex')


def test_drop_indexes_exists():
    """Test that DataArray.drop_indexes method exists."""
    da = DataArray([1, 2, 3], coords={'x': [0, 1, 2]}, dims='x')
    assert hasattr(da, 'drop_indexes')


def test_dataset_set_xindex_exists():
    """Test that Dataset.set_xindex method exists."""
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    assert hasattr(ds, 'set_xindex')


def test_dataset_drop_indexes_exists():
    """Test that Dataset.drop_indexes method exists."""
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    assert hasattr(ds, 'drop_indexes')