"""
Regression test for issue where merge(combine_attrs='override') does not copy attrs 
but instead references attrs from the first object.

This test ensures that when merge is called with combine_attrs='override', 
the returned attributes are independent copies, not references to the original objects.
"""

import xarray as xr


def test_merge_override_attrs_are_copied_not_referenced():
    """Test that merged attrs with combine_attrs='override' are independent copies."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override' 
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged result has the expected attrs (from first dataset)
    assert xds3.attrs['a'] == 'b'
    
    # Now modify the merged attrs - this should NOT affect the original datasets
    xds3.attrs['a'] = 'd'
    
    # Check that the original datasets are unchanged
    assert xds1.attrs['a'] == 'b'  # Should still be 'b', not 'd'
    assert xds2.attrs['a'] == 'c'  # Should still be 'c', not 'd'
    assert xds3.attrs['a'] == 'd'  # Merged dataset should have 'd'


def test_merge_override_attrs_multiple_attributes():
    """Test that multiple attributes are handled correctly."""
    # Create two datasets with multiple different attrs
    xds1 = xr.Dataset(attrs={'a': 'b', 'c': 'd'})
    xds2 = xr.Dataset(attrs={'a': 'e', 'c': 'f'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds1.attrs['c'] == 'd'
    assert xds2.attrs['a'] == 'e'
    assert xds2.attrs['c'] == 'f'
    
    # Merge with combine_attrs='override' 
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged result has the expected attrs (from first dataset)
    assert xds3.attrs['a'] == 'b'
    assert xds3.attrs['c'] == 'd'
    
    # Now modify the merged attrs
    xds3.attrs['a'] = 'new_b'
    xds3.attrs['c'] = 'new_d'
    
    # Check that the original datasets are unchanged
    assert xds1.attrs['a'] == 'b'
    assert xds1.attrs['c'] == 'd'
    assert xds2.attrs['a'] == 'e'
    assert xds2.attrs['c'] == 'f'
    
    # Check that the merged dataset has the new values
    assert xds3.attrs['a'] == 'new_b'
    assert xds3.attrs['c'] == 'new_d'


def test_merge_override_attrs_no_conflicts_same_keys():
    """Test behavior with same key names but different values."""
    xds1 = xr.Dataset(attrs={'x': 'first', 'y': 'first'})
    xds2 = xr.Dataset(attrs={'x': 'second', 'y': 'second'})
    
    # Verify initial state
    assert xds1.attrs['x'] == 'first'
    assert xds1.attrs['y'] == 'first'
    assert xds2.attrs['x'] == 'second'
    assert xds2.attrs['y'] == 'second'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Should contain first dataset's attrs
    assert xds3.attrs['x'] == 'first'
    assert xds3.attrs['y'] == 'first'
    
    # Modify merged attrs
    xds3.attrs['x'] = 'modified'
    
    # Original datasets should remain unchanged
    assert xds1.attrs['x'] == 'first'
    assert xds2.attrs['x'] == 'second'
    assert xds3.attrs['x'] == 'modified'