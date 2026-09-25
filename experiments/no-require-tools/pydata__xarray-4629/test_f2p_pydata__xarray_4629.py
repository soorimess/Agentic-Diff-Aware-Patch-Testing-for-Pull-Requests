"""
Test for the regression: merge(combine_attrs='override') should copy attrs
instead of referencing them from the first object.

This test ensures that after a merge with combine_attrs='override',
modifications to the merged result's attributes don't affect the source datasets.
"""
import xarray as xr


def test_merge_override_attrs_are_copied_not_referenced():
    """Test that merge with combine_attrs='override' copies attrs, not references them."""
    # Create test datasets with different attribute values
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Verify initial states
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Perform merge with combine_attrs='override' 
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify merge result has the expected attrs (from first dataset)
    assert xds3.attrs['a'] == 'b'
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    # Modify the merged result's attributes
    xds3.attrs['a'] = 'd'
    
    # After modification, the merged dataset's attrs should reflect the change
    assert xds3.attrs['a'] == 'd'
    
    # BUT the original source datasets should NOT be affected
    # This is the bug: if attrs are referenced (not copied), this will fail
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'


def test_merge_override_attrs_independence_of_source_datasets():
    """Test that modifications to merged attrs don't affect different source attrs."""
    # Create test datasets with different attribute values
    xds1 = xr.Dataset(attrs={'test_attr': 'original1'})
    xds2 = xr.Dataset(attrs={'test_attr': 'original2'})
    
    # Perform merge 
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Verify initial state
    assert xds3.attrs['test_attr'] == 'original1'  # From first dataset
    
    # Change merged attrs
    xds3.attrs['test_attr'] = 'modified'
    
    # Original datasets should remain unchanged
    assert xds1.attrs['test_attr'] == 'original1'
    assert xds2.attrs['test_attr'] == 'original2'


def test_exact_bug_report_example():
    """Test using the exact example from the bug report."""
    # Exact example from bug report
    xds1 = xr.Dataset(attrs={'a': 'b'})
    xds2 = xr.Dataset(attrs={'a': 'c'})
    
    # Print initial values (as in bug report)
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    
    xds3 = xr.merge([xds1, xds2], combine_attrs='override')
    
    # Check the values after merge
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'
    assert xds3.attrs['a'] == 'b'
    
    # The critical test - mutate the merged result
    xds3.attrs['a'] = 'd'
    
    # The bug: this assertion would fail if attrs are referenced rather than copied
    # After modifying xds3, xds1 should still have 'b', not 'd'
    assert xds1.attrs['a'] == 'b'
    assert xds2.attrs['a'] == 'c'  
    assert xds3.attrs['a'] == 'd'