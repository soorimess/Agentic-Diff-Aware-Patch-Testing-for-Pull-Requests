import xarray as xr


def test_merge_combine_attrs_override_copy_attrs():
    """
    Test that merge with combine_attrs='override' copies attrs rather than referencing them.
    
    This is a regression test for a bug where merge(combine_attrs='override') would
    store a reference to the first dataset's attrs instead of creating a copy.
    """
    # Create two datasets with different attrs
    ds1 = xr.Dataset(attrs={'a': 'b'})
    ds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert ds1.attrs['a'] == 'b'
    assert ds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    
    # Verify the merged result has the first dataset attributes
    assert merged.attrs['a'] == 'b'
    
    # The critical test: modifying merged attrs should not affect source attrs
    # This would happen if merged.attrs was referencing the same dict as ds1.attrs
    merged.attrs['a'] = 'd'
    
    # After the fix, source attrs should remain unchanged
    assert ds1.attrs['a'] == 'b'  # This would fail if bug existed
    assert ds2.attrs['a'] == 'c'  # This should be unchanged
    assert merged.attrs['a'] == 'd'  # This should be 'd'