"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.
"""
import xarray as xr


def test_merge_override_attrs_are_independent():
    """Test that attrs of merged result are independent from source datasets."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs are initially correct
    assert xds3.attrs['a'] == 'b'  # Should take from first dataset
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'd'
    
    # The source datasets should NOT be affected
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_dict_copy():
    """Test that merge_attrs with combine_attrs='override' returns a copy, not reference."""
    from xarray.core.merge import merge_attrs
    
    # Test the specific function that was changed
    attrs_list = [{'a': 'b'}, {'a': 'c'}]
    
    # This should return a copy, not a reference to the first dict
    result = merge_attrs(attrs_list, 'override')
    
    # Modify the result
    result['a'] = 'modified'
    
    # Original should not be affected
    assert attrs_list[0]['a'] == 'b'
    assert result['a'] == 'modified'