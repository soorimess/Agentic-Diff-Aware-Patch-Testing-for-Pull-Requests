import xarray as xr


def test_merge_combine_attrs_override_independent_attrs():
    """Test that merge with combine_attrs='override' returns independent attrs dict.
    
    This is a regression test for the bug where merge(combine_attrs='override') 
    would return a reference to the first source's attrs dict instead of a copy.
    
    Before the fix: modifying merged attrs would affect source attrs
    After the fix: merged attrs and source attrs are independent
    """
    # Create two datasets with different attrs as per the bug report
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override (this is where the bug occurs)
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs are correct
    assert xds3.attrs['a'] == 'b'  # Should be from first dataset
    
    # Modify the merged attrs - this should NOT affect source attrs
    xds3.attrs['a'] = 'd'
    
    # The key test: source attrs should remain unchanged
    # This would fail before the fix because xds1.attrs['a'] would be 'd' instead of 'b'
    assert xds1.attrs['a'] == 'b', f"Source attrs were modified: expected 'b', got '{xds1.attrs['a']}'"
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'