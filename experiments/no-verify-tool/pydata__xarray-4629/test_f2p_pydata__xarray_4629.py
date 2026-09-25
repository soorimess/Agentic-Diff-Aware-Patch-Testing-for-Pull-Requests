"""
Test for merge(combine_attrs='override') bug.
Tests that attrs are properly copied and not referenced from the first object.
"""
import xarray as xr


def test_merge_override_attrs_copy_not_reference():
    """Test that merge with combine_attrs='override' copies attrs instead of referencing them."""
    # Create two datasets with different attrs
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override' 
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged result has the expected attrs 
    assert xds3.attrs['a'] == 'b'  # Should get attrs from first dataset
    
    # Modify the merged dataset's attrs
    xds3.attrs['a'] = 'd'
    
    # After modification, the original datasets should NOT be affected
    # This is the bug: in the buggy version, xds1.attrs['a'] would change to 'd'
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'd'


def test_merge_override_attrs_copy_not_reference_deep_modify():
    """Test deep modification of merged attrs doesn't affect source datasets."""
    # Create two datasets with nested dict attrs
    xds1 = xr.Dataset(attrs={'nested': {'key': 'value1'}})
    xds2 = xr.Dataset(attrs={'nested': {'key': 'value2'}})
    
    # Verify initial state
    assert xds1.attrs['nested']['key'] == 'value1'
    assert xds2.attrs['nested']['key'] == 'value2'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged result has the expected attrs
    assert xds3.attrs['nested']['key'] == 'value1'  # Should get attrs from first dataset
    
    # Modify the merged dataset's nested attrs
    xds3.attrs['nested']['key'] = 'value3'
    
    # After modification, the original datasets should NOT be affected
    # This is the bug: in the buggy version, xds1.attrs['nested']['key'] would change to 'value3'
    assert xds1.attrs['nested']['key'] == 'value1'
    assert xds2.attrs['nested']['key'] == 'value2' 
    assert xds3.attrs['nested']['key'] == 'value3'


def test_merge_override_attrs_mutation_independent():
    """Test that merged attrs can be mutated independently of source datasets."""
    # Create two datasets with same attrs to test independent mutation
    xds1 = xr.Dataset(attrs={'x': 1, 'y': 2})
    xds2 = xr.Dataset(attrs={'x': 2, 'y': 3})
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merged has the first dataset's attrs
    assert xds3.attrs['x'] == 1
    assert xds3.attrs['y'] == 2
    
    # Mutate the merged attrs independently
    xds3.attrs['z'] = 3  # Add new attribute
    xds3.attrs['x'] = 10  # Change existing attribute
    
    # Original datasets should remain unchanged
    assert xds1.attrs['x'] == 1
    assert xds1.attrs['y'] == 2
    assert xds2.attrs['x'] == 2
    assert xds2.attrs['y'] == 3
    
    # Merged dataset should have the modifications
    assert xds3.attrs['x'] == 10
    assert xds3.attrs['y'] == 2
    assert xds3.attrs['z'] == 3
    
    # Check that xds1 and xds2 have independent dicts
    assert xds1.attrs is not xds3.attrs
    assert xds2.attrs is not xds3.attrs