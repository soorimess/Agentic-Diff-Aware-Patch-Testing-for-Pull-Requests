"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.

This test ensures that after a merge with combine_attrs='override', 
the merged dataset's attrs are independent from the source datasets.
"""

import xarray as xr


def test_merge_override_attrs_are_copied():
    """Test that attrs from merged dataset are independent of source datasets."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override combine_attrs
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged attrs are set correctly
    assert xds3.attrs['a'] == 'b'  # Should be from first dataset
    
    # The critical test: modify the merged attrs and ensure source attrs are unchanged
    original_xds1_attrs = dict(xds1.attrs)
    original_xds2_attrs = dict(xds2.attrs)
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'd'
    
    # The source datasets should be unchanged
    assert xds1.attrs['a'] == original_xds1_attrs['a']  # Still 'b'
    assert xds2.attrs['a'] == original_xds2_attrs['a']  # Still 'c'
    
    # The merged dataset should have the new value
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_multiple_changes():
    """Test multiple attribute modifications don't affect source datasets."""
    xds1 = xr.Dataset(attrs={'a': 'b', 'c': 'd'})
    xds2 = xr.Dataset(attrs={'a': 'e', 'f': 'g'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'e'
    
    # Merge with override combine_attrs - should take attrs from first dataset
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged attrs are set correctly (from first dataset)
    assert xds3.attrs['a'] == 'b'  # Should be from first dataset
    assert xds3.attrs['c'] == 'd'  # Should be from first dataset
    # Note: xds2.attrs['f'] should NOT be in merged attrs with 'override'
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'new_value'
    xds3.attrs['c'] = 'new_c'
    xds3.attrs['new_key'] = 'new_value_2'
    
    # The source datasets should be unchanged
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'e'
    assert xds1.attrs['c'] == 'd'
    # xds2.attrs['f'] is not in the merged result, so we don't check it
    
    # The merged dataset should have the new values
    assert xds3.attrs['a'] == 'new_value'
    assert xds3.attrs['c'] == 'new_c'
    assert xds3.attrs['new_key'] == 'new_value_2'