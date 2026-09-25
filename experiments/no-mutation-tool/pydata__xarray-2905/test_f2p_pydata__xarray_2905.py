"""
Regression test for issue where Variable.__setitem__ coerces types on objects 
with a values property when not using pandas objects.

This test verifies the fix for a regression introduced in v0.10.1 where 
objects with a 'values' attribute were incorrectly coerced to their values
instead of being stored as the objects themselves.
"""
import numpy as np
import xarray as xr


def test_objects_with_values_property_preserved():
    """
    Test that objects with 'values' property are stored as the objects themselves,
    not their .values attribute.
    
    Before fix (buggy behavior): assigning HasValues() with values=5 
    resulted in storing the value 5 (scalar) in the object array.
    
    After fix (correct behavior): assigning HasValues() with values=5 
    results in storing the HasValues object itself in the object array.
    """
    # Create a data array that will result in object dtype
    arr = xr.DataArray([None])
    
    # Create an object with a values property
    class HasValues(object):
        values = 5
    
    # This should store the HasValues object itself, not extract its .values attribute
    arr.loc[{'dim_0': 0}] = HasValues()
    
    # In the buggy behavior we would get: array([5]) - the scalar 5
    # In the fixed behavior we should get: array([HasValues_instance]) - the object
    first_element = arr.values[0]
    
    # Assert that we have the object itself, not the .values attribute
    assert isinstance(first_element, HasValues), f"Expected HasValues object, got {type(first_element)}"
    assert first_element.values == 5, "Object should preserve its values attribute"


def test_exact_bug_report_example():
    """
    Test the exact example from the bug report.
    """
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This is the exact line from the bug report that was problematic
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # In the FIXED behavior, this should provide:
    # bad_indexed.values => array([< __main__.HasValues instance>], dtype=object)
    
    # Check that we get the HasValues object, not array(5)
    assert isinstance(bad_indexed.values[0], HasValues)
    assert bad_indexed.values[0].values == 5


def test_pandas_objects_behavior_unchanged():
    """
    Test that pandas objects still get their .values extracted for backward compatibility.
    This validates that the behavior for pandas objects is preserved.
    """
    # A more careful approach to test pandas behavior - we have to use the actual 
    # as_compatible_data function to test pandas paths
    
    from xarray.core.variable import as_compatible_data
    import pandas as pd

    # Create pandas Series
    series = pd.Series([1, 2, 3])
    
    # Function call should extract the values 
    result = as_compatible_data(series)
    
    # For pandas Series, the result should equal the .values array 
    expected = series.values
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, expected)