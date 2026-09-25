"""
Regression test for issue where merge(combine_attrs='override') does not
copy attrs but instead references attrs from the first object
"""
import xarray as xr


def test_merge_override_does_not_reference_attrs():
    """Test that merge with combine_attrs='override' returns a copy, not reference."""
    # Create two datasets with different attrs (as shown in the bug report)
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with override
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify that merged attrs are correctly set
    assert xds3.attrs['a'] == 'b'  # Should come from first dataset
    
    # Test that modifying the merged result doesn't affect the source datasets
    original_xds1_attrs = dict(xds1.attrs)
    original_xds2_attrs = dict(xds2.attrs)
    
    # Modify the merged dataset attributes
    xds3.attrs['a'] = 'd'
    
    # The source datasets should NOT be affected
    assert xds1.attrs['a'] == original_xds1_attrs['a']  # Still 'b'
    assert xds2.attrs['a'] == original_xds2_attrs['a']  # Still 'c'
    
    # The merged dataset should have the new value
    assert xds3.attrs['a'] == 'd'