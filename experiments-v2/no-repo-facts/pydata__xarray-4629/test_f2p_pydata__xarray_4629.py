import xarray as xr


def test_merge_combine_attrs_override_does_not_reference_source_attrs():
    """Test that merge with combine_attrs='override' creates a copy of attrs, not a reference."""
    # Create datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial values
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs are correct
    assert xds3.attrs['a'] == 'b'  # Should be from first dataset
    
    # Modify the merged attrs
    xds3.attrs['a'] = 'd'
    
    # The original datasets should NOT be affected
    assert xds1.attrs['a'] == 'b'  # Should still be 'b'
    assert xds2.attrs['a'] == 'c'  # Should still be 'c'
    assert xds3.attrs['a'] == 'd'  # Should be 'd'


def test_merge_combine_attrs_override_attrs_are_independent():
    """Test that modifying attrs in merged dataset doesn't affect source datasets."""
    # Create datasets with same attr key but different values
    xds1 = xr.Dataset(attrs={'key': 'value1'})
    xds2 = xr.Dataset(attrs={'key': 'value2'})
    
    # Merge with override
    merged = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Store original values
    original_xds1_key = xds1.attrs['key']
    original_xds2_key = xds2.attrs['key']
    original_merged_key = merged.attrs['key']
    
    # Modify merged attrs
    merged.attrs['key'] = 'modified'
    
    # Check that original datasets are unchanged
    assert xds1.attrs['key'] == original_xds1_key
    assert xds2.attrs['key'] == original_xds2_key
    assert merged.attrs['key'] == 'modified'