import pytest
import xarray as xr


def test_merge_combine_attrs_override_does_not_reference_source_attrs():
    """Test that merge with combine_attrs='override' does not reference source attributes.
    
    Bug: When using combine_attrs='override', the merged result's attrs reference
    the attrs from the first source object instead of creating a copy.
    This causes modifications to the merged attrs to affect the original source attrs.
    """
    # Create two datasets with different attributes
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial state
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Merge with combine_attrs='override'
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify the merged attrs value (should be from first dataset)
    assert xds3.attrs['a'] == 'b'
    
    # Verify that attrs are actually copied, not referenced
    # Modify the merged attrs
    xds3.attrs['a'] = 'd'
    
    # The source dataset attrs should remain unchanged
    assert xds1.attrs['a'] == 'b'  # This should still be 'b'
    assert xds2.attrs['a'] == 'c'  # This should still be 'c'
    assert xds3.attrs['a'] == 'd'  # This should be 'd'


def test_merge_combine_attrs_override_attrs_mutation_independent():
    """Additional test to ensure attrs of merged result can be modified independently."""
    # Create datasets with the same attribute key but different values
    ds1 = xr.Dataset(attrs={'x': 'original1', 'y': 'shared'})
    ds2 = xr.Dataset(attrs={'x': 'original2', 'z': 'shared'})
    
    # Merge with override logic
    result = xr.merge([ds1, ds2], combine_attrs='override')
    
    # Test that changing result's attrs doesn't affect source datasets
    original_ds1_x = ds1.attrs['x'] 
    original_ds2_x = ds2.attrs['x'] 
    
    # Modify attrs of the merged result
    result.attrs['x'] = 'modified'
    result.attrs['new_attr'] = 'added'
    
    # Source datasets should be unchanged
    assert ds1.attrs['x'] == original_ds1_x
    assert ds2.attrs['x'] == original_ds2_x
    assert 'new_attr' not in ds1.attrs
    assert 'new_attr' not in ds2.attrs
    
    # Result should have modified attrs
    assert result.attrs['x'] == 'modified'
    assert result.attrs['new_attr'] == 'added'