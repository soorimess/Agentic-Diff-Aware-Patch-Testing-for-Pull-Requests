"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.

This test ensures that when combine_attrs='override' is used, the attributes
of the merged result are independent from the source datasets - changes to
the merged result's attributes should not affect the source datasets.
"""

import xarray as xr


def test_merge_override_attrs_are_independent():
    """Test that attributes in merged result are independent from source datasets."""
    # Create two datasets with different attribute values
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial values
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged result has the first dataset's attribute value
    assert xds3.attrs['a'] == 'b'
    
    # Verify that modifying the merged result's attributes doesn't affect the source datasets
    original_xds1_attrs = dict(xds1.attrs)
    original_xds2_attrs = dict(xds2.attrs)
    
    # Modify the merged result's attributes
    xds3.attrs['a'] = 'd'
    
    # The source datasets should be unchanged
    assert xds1.attrs['a'] == original_xds1_attrs['a']  # Should still be 'b'
    assert xds2.attrs['a'] == original_xds2_attrs['a']  # Should still be 'c'
    
    # The merged result should have the new value
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_dict_mutation():
    """Test that modifying the attributes dict directly doesn't affect sources."""
    # Create two datasets with different attribute values
    xds1 = xr.Dataset(attrs={'a': 'b', 'c': 'd'})
    xds2 = xr.Dataset(attrs={'a': 'e', 'f': 'g'})
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify initial state
    assert xds3.attrs['a'] == 'b'
    assert xds3.attrs['c'] == 'd'
    
    # Get reference to the attrs dict from the merged result
    merged_attrs = xds3.attrs
    
    # Modify the attrs dict directly
    merged_attrs['a'] = 'modified'
    merged_attrs['new_key'] = 'new_value'
    
    # The source datasets should be unchanged
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'e'
    
    # The merged result should have the modified values
    assert xds3.attrs['a'] == 'modified'
    assert xds3.attrs['new_key'] == 'new_value'