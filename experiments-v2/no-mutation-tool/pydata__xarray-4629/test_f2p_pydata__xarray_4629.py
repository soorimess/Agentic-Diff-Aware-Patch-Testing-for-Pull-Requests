import xarray as xr


def test_merge_combine_attrs_override_does_not_share_attrs():
    """Test that merge with combine_attrs='override' does not share attribute references.
    
    This is a regression test for the bug where merge(combine_attrs='override') 
    would return a reference to the first dataset's attrs dict instead of a copy,
    causing changes to the merged result to affect the source datasets.
    """
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override combine_attrs
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs are correct
    assert xds3.attrs['a'] == 'b'  # Should take first dataset's attrs
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'd'
    
    # The original datasets should NOT be affected
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_combine_attrs_override_attrs_independence():
    """Additional test to ensure attrs independence in more complex scenarios."""
    # Create datasets with multiple attributes
    xds1 = xr.Dataset(attrs={'attr1': 'value1', 'attr2': 'value2'})
    xds2 = xr.Dataset(attrs={'attr1': 'value3', 'attr3': 'value4'})
    
    # Merge with override combine_attrs
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify initial merged state
    assert xds3.attrs['attr1'] == 'value1'  # From first dataset
    assert xds3.attrs['attr2'] == 'value2'  # From first dataset  
    assert 'attr3' not in xds3.attrs  # Not in first dataset
    
    # Modify merged attrs
    xds3.attrs['attr1'] = 'modified'
    xds3.attrs['new_attr'] = 'new_value'
    
    # Original datasets should be unchanged
    assert xds1.attrs['attr1'] == 'value1'
    assert xds1.attrs['attr2'] == 'value2'
    assert xds2.attrs['attr1'] == 'value3'
    assert xds2.attrs['attr3'] == 'value4'
    
    # Merged dataset should have modified values
    assert xds3.attrs['attr1'] == 'modified'
    assert xds3.attrs['new_attr'] == 'new_value'