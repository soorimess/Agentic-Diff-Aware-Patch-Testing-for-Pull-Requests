"""
Regression test for the bug where merge(combine_attrs='override') 
does not copy attrs but instead references attrs from the first object.
"""
import xarray as xr


def test_merge_override_does_not_reference_attrs():
    """Test that merge with combine_attrs='override' creates a copy of attrs, not a reference."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged result has the expected attrs
    assert xds3.attrs['a'] == 'b'  # Should take from first dataset
    
    # The critical test: modify the merged attrs and ensure original datasets are not affected
    xds3.attrs['a'] = 'd'
    
    # After modifying merged attrs, original datasets should be unchanged
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_isolated():
    """Test that modifying attrs on merged result doesn't affect source datasets."""
    # Create datasets with same attr names but different values
    ds1 = xr.Dataset({'data': [1, 2, 3]}, attrs={'version': '1.0', 'author': 'test1'})
    ds2 = xr.Dataset({'data': [4, 5, 6]}, attrs={'version': '2.0', 'author': 'test2'})
    
    # Merge with override
    merged = xr.merge([ds1, ds2], combine_attrs='override')
    
    # Verify initial state
    assert merged.attrs['version'] == '1.0'
    assert merged.attrs['author'] == 'test1'
    assert ds1.attrs['version'] == '1.0'
    assert ds2.attrs['version'] == '2.0'
    
    # Modify merged attrs
    merged.attrs['version'] = 'modified'
    merged.attrs['new_attr'] = 'added'
    
    # Original datasets should be unchanged
    assert ds1.attrs['version'] == '1.0'
    assert ds2.attrs['version'] == '2.0'
    assert ds1.attrs['author'] == 'test1'
    assert ds2.attrs['author'] == 'test2'
    
    # Merged should have updated attrs
    assert merged.attrs['version'] == 'modified'
    assert merged.attrs['author'] == 'test1'
    assert merged.attrs['new_attr'] == 'added'