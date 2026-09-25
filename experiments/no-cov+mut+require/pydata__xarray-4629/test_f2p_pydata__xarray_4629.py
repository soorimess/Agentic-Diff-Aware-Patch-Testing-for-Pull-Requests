"""
Regression test for bug where merge(combine_attrs='override') does not copy attrs
but instead references attrs from the first object.

This test verifies that when merging datasets with combine_attrs='override',
the resulting merged dataset has its own copy of attributes that can be modified
independently of the source datasets.
"""
import xarray as xr


def test_merge_combine_attrs_override_creates_copy():
    """Test that combine_attrs='override' creates a copy of attributes, not a reference."""
    # Create two datasets with different attribute values
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial attribute values
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged dataset gets the first dataset's attribute
    assert xds3.attrs['a'] == 'b'
    
    # Modify the merged dataset's attributes
    xds3.attrs['a'] = 'd'
    
    # The modification should NOT affect the original datasets
    # This is the bug: in the buggy version, xds1.attrs['a'] would become 'd'
    assert xds1.attrs['a'] == 'b', "Original dataset attrs were modified when they shouldn't be"
    assert xds2.attrs['a'] == 'c', "Second original dataset attrs were modified when they shouldn't be"
    assert xds3.attrs['a'] == 'd', "Merged dataset attrs were correctly modified"


def test_merge_combine_attrs_override_attrs_independence():
    """Test that modifying individual attributes doesn't affect other datasets."""
    # Create datasets with multiple attributes
    xds1 = xr.Dataset(attrs={'attr1': 'value1', 'attr2': 'value2'})
    xds2 = xr.Dataset(attrs={'attr1': 'value3', 'attr2': 'value4'})
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify initial state
    assert xds1.attrs['attr1'] == 'value1'
    assert xds2.attrs['attr1'] == 'value3'
    assert xds3.attrs['attr1'] == 'value1'  # Should get first dataset's attr
    
    # Modify merged dataset independently
    xds3.attrs['attr1'] = 'modified'
    
    # Verify independence
    assert xds1.attrs['attr1'] == 'value1', "First original was affected by modification"
    assert xds2.attrs['attr1'] == 'value3', "Second original was affected by modification"
    assert xds3.attrs['attr1'] == 'modified', "Merged dataset was not modified correctly"