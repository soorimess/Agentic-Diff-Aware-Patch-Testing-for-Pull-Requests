import xarray as xr


def test_merge_combine_attrs_override_copies_attrs():
    """Test that merge with combine_attrs='override' copies attrs instead of referencing them."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial values
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged dataset has the right attrs from the first dataset
    assert xds3.attrs['a'] == 'b'
    
    # The bug: modification of merged attrs affects source datasets
    # This should NOT happen - merged attrs should be independent
    xds3.attrs['a'] = 'd'
    
    # After changing the merged dataset's attrs, the source datasets should NOT change
    assert xds1.attrs['a'] == 'b'  # This will fail in the buggy version
    assert xds2.attrs['a'] == 'c'  # This should remain unchanged
    assert xds3.attrs['a'] == 'd'  # This should be the new value


def test_merge_combine_attrs_override_preserves_original_attrs():
    """Test that the original attr dicts are not modified when merging with override."""
    # Create test datasets
    xds1 = xr.Dataset(attrs={'a': 'b', 'c': 'd'})
    xds2 = xr.Dataset(attrs={'a': 'e', 'f': 'g'})
    
    # Store references to the original attrs
    original_attrs1 = xds1.attrs
    original_attrs2 = xds2.attrs
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # The merged attrs should be independent, not references to the original
    xds3.attrs['a'] = 'new_value'
    xds3.attrs['h'] = 'i'
    
    # Original attrs should be unchanged
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'e'
    assert xds1.attrs['c'] == 'd'
    assert xds2.attrs['f'] == 'g'
    
    # The merged attrs should reflect our changes
    assert xds3.attrs['a'] == 'new_value'
    assert xds3.attrs['h'] == 'i'