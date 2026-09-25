"""
Regression test for xarray merge attrs bug.

This test ensures that merge(combine_attrs='override') returns a copy of
attributes rather than a reference, so that modifying attributes of the 
merged result does not affect the source datasets.
"""

import xarray as xr


def test_merge_override_attrs_independent():
    """Test that merged attrs are independent of source attrs when using combine_attrs='override'."""
    # Create two datasets with different attributes
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged attrs are from first dataset 
    assert xds3.attrs['a'] == 'b'
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'd'
    
    # After modification, the merged result should have the new value
    assert xds3.attrs['a'] == 'd'
    
    # BUT the source datasets should NOT be affected
    # This is the bug being fixed - previously both xds1 and xds3 would have 'd'
    assert xds1.attrs['a'] == 'b'  # This should still be 'b' after modifying xds3
    assert xds2.attrs['a'] == 'c'  # This should still be 'c'
    
    # Additional verification - the attrs should be independent objects
    assert xds1.attrs is not xds3.attrs
    assert xds2.attrs is not xds3.attrs


def test_merge_override_attrs_copy_behavior():
    """Test that the merged attrs dict is actually a copy, not a reference."""
    xds1 = xr.Dataset(attrs={'key': 'value1', 'other': 'data'})
    xds2 = xr.Dataset(attrs={'key': 'value2', 'another': 'info'})
    
    # Merge with override
    merged = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Check that we can modify merged attrs without affecting sources
    original_xds1_attrs = xds1.attrs
    original_xds2_attrs = xds2.attrs
    original_merged_attrs = merged.attrs
    
    # Modify the merged attrs
    merged.attrs['key'] = 'modified'
    merged.attrs['new_key'] = 'new_value'
    
    # Verify that original sources are unchanged
    assert xds1.attrs['key'] == 'value1'
    assert xds2.attrs['key'] == 'value2'
    assert xds1.attrs['other'] == 'data'
    assert xds2.attrs['another'] == 'info'
    
    # Verify that merged attrs were actually changed
    assert merged.attrs['key'] == 'modified'
    assert merged.attrs['new_key'] == 'new_value'
    
    # Verify they are different objects
    assert merged.attrs is not xds1.attrs
    assert merged.attrs is not xds2.attrs