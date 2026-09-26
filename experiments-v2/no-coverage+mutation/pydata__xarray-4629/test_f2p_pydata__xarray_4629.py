"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.

This test ensures that when combine_attrs='override' is used, the merged result
has its own copy of attributes that can be modified without affecting the source
datasets.
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
    
    # Merge with override combine_attrs
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged result has the right attribute value
    assert xds3.attrs['a'] == 'b'  # Should take from first dataset
    
    # Modify the merged result's attrs
    xds3.attrs['a'] = 'd'
    
    # The original datasets should NOT be affected
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # The merged result should have the new value
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_mutation_independent():
    """Test that modifying attrs in one dataset doesn't affect others after merge."""
    # Create datasets with same attr name but different values
    xds1 = xr.Dataset(attrs={'test_attr': 'value1'})
    xds2 = xr.Dataset(attrs={'test_attr': 'value2'})
    xds3 = xr.Dataset(attrs={'test_attr': 'value3'})
    
    # Merge them
    merged = xr.merge([xds1, xds2, xds3], combine_attrs='override')
    
    # Verify initial state
    assert merged.attrs['test_attr'] == 'value1'  # Should come from first
    
    # Modify the merged attrs
    merged.attrs['test_attr'] = 'modified_value'
    
    # Original datasets should be unchanged
    assert xds1.attrs['test_attr'] == 'value1'
    assert xds2.attrs['test_attr'] == 'value2'
    assert xds3.attrs['test_attr'] == 'value3'
    
    # Merged should have the new value
    assert merged.attrs['test_attr'] == 'modified_value'