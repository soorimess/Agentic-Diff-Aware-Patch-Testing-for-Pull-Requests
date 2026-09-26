import xarray as xr


def test_merge_combine_attrs_override_does_not_reference_attrs():
    """Test that merge with combine_attrs='override' creates a copy of attrs, not a reference.
    
    This reproduces the exact example from the bug report:
    After a merge, an attribute value change in the merged product is reflected 
    in the first source.
    
    Before the fix, the line `return variable_attrs[0]` would return a reference
    to the first dataset's attrs dict, causing side effects.
    """
    # Reproduce the exact example from the bug report
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override (this is where the bug occurs)
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs
    assert xds3.attrs['a'] == 'b'  # Should take first dataset's attrs
    
    # This is the key test: modifying the merged attrs should NOT affect source datasets
    xds3.attrs['a'] = 'd'
    
    # Before fix: xds1.attrs['a'] would be 'd' (incorrect)
    # After fix: xds1.attrs['a'] should still be 'b' (correct)
    assert xds1.attrs['a'] == 'b', f"Source dataset attrs were incorrectly modified: {xds1.attrs['a']}"
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_combine_attrs_override_preserves_original_attrs_dicts():
    """Test that the merged result has its own copy of attrs dict, not a reference."""
    # Create datasets with same attr names but different values
    xds1 = xr.Dataset(attrs={'test_attr': 'value1'})
    xds2 = xr.Dataset(attrs={'test_attr': 'value2'})
    
    # Merge with override
    merged = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Store reference to first dataset's attrs
    original_xds1_attrs = xds1.attrs
    
    # Modify the merged attrs
    merged.attrs['test_attr'] = 'modified_value'
    
    # The original attrs should not be affected
    assert xds1.attrs['test_attr'] == 'value1'
    assert xds2.attrs['test_attr'] == 'value2'
    
    # The merged attrs should have the new value
    assert merged.attrs['test_attr'] == 'modified_value'
    
    # Verify that we're working with different dict objects
    assert merged.attrs is not original_xds1_attrs