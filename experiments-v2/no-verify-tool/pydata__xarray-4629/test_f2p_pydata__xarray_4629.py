"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.
"""
import xarray as xr


def test_merge_override_does_not_reference_attrs():
    """Test that merge with combine_attrs='override' creates a copy, not a reference."""
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
    
    # Modify the merged result's attrs
    xds3.attrs['a'] = 'd'
    
    # The original datasets should NOT be affected
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_deep_copy():
    """Test that the attrs dict is actually a copy, not a reference."""
    # Create datasets with nested attrs to test deep copying
    xds1 = xr.Dataset(attrs={'nested': {'key': 'value1'}})
    xds2 = xr.Dataset(attrs={'nested': {'key': 'value2'}})
    
    # Merge with override
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Modify nested structure in merged result
    xds3.attrs['nested']['key'] = 'modified'
    
    # Original datasets should NOT be affected
    assert xds1.attrs['nested']['key'] == 'value1'
    assert xds2.attrs['nested']['key'] == 'value2'
    assert xds3.attrs['nested']['key'] == 'modified'