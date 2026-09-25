import xarray as xr


def test_merge_combine_attrs_override_creates_copy():
    """Test that merge with combine_attrs='override' creates a copy of attrs, not a reference.
    
    This reproduces the bug where modifying attrs of the merged result affects
    the source datasets.
    """
    # Create two datasets with different attrs - exactly as in the bug report
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Test exactly as described in the bug report
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the reported values
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'  
    assert xds3.attrs['a'] == 'b'
    
    # This is the key test - modify merged attrs and ensure source is unaffected
    xds3.attrs['a'] = 'd'
    
    # The bug: this would fail, meaning xds1.attrs['a'] would be 'd' instead of 'b'
    assert xds1.attrs['a'] == 'b', "Source dataset xds1.attrs['a'] was modified unexpectedly!"
    assert xds2.attrs['a'] == 'c', "Source dataset xds2.attrs['a'] was modified unexpectedly!"
    
    # The merged dataset should reflect the change
    assert xds3.attrs['a'] == 'd'