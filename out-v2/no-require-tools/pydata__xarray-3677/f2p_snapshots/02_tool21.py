"""
Regression test for issue where merging a DataArray into a Dataset using 
the Dataset.merge() method fails.
"""
import xarray as xr


def test_merge_dataarray_into_dataset():
    """Test that merging a DataArray into a Dataset works correctly."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails with AttributeError
    # 'DataArray' object has no attribute 'items'
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert expected.equals(actual)
    
    # Verify the result has the expected structure
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1


def test_merge_dataarray_into_dataset_with_coords():
    """Test merging a DataArray with coordinates into a Dataset."""
    ds = xr.Dataset({'a': [1, 2, 3]})
    da = xr.DataArray([4, 5, 6], dims=['x'], name='b')
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails with AttributeError
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert expected.equals(actual)
    
    # Verify the result has the expected structure
    assert 'a' in actual
    assert 'b' in actual
    assert len(actual['b']) == 3


def test_merge_dataarray_into_dataset_with_attrs():
    """Test merging a DataArray with attributes into a Dataset."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b', attrs={'units': 'm'})
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails with AttributeError
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert expected.equals(actual)
    
    # Verify the result has the expected structure
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1
    assert actual['b'].attrs['units'] == 'm'