import pytest

import pandas as pd
from pandas import DataFrame, concat


def test_concat_validation_refactored_from_concatenator_class():
    """
    Regression test for PR #59141: Make concat not stateful.
    
    This test ensures that validation logic for concat parameters (join, sort)
    works correctly after the refactoring that moved validation from the 
    _Concatenator class to the main concat function.
    
    The PR makes concat not stateful by removing the _Concatenator class and
    inlining the validation logic.
    """
    df1 = DataFrame({"A": [1, 2]})
    df2 = DataFrame({"A": [3, 4]})
    
    # Test valid join values work correctly
    result_outer = concat([df1, df2], join="outer")
    result_inner = concat([df1, df2], join="inner")
    
    # Test invalid join raises proper error with exact message
    with pytest.raises(ValueError, match="Only can inner.*outer"):
        concat([df1, df2], join="invalid_join_value")
    
    # Test valid sort values work correctly
    result_false = concat([df1, df2], sort=False)
    result_true = concat([df1, df2], sort=True)
    
    # Test invalid sort raises proper error with exact message
    with pytest.raises(ValueError, match="The 'sort' keyword only accepts boolean values"):
        concat([df1, df2], sort="not_a_boolean")
        
    # Test empty input raises proper error
    with pytest.raises(ValueError, match="No objects to concatenate"):
        concat([])


def test_concat_single_object_rejection():
    """
    Test that single pandas objects are properly rejected (PR #59141 validation).
    
    This ensures that the validation logic for rejecting single Series/DataFrame
    objects was properly moved from _Concatenator to main concat function.
    """
    df = DataFrame({"A": [1, 2]})
    series = pd.Series([1, 2])
    
    # Test that single DataFrame is rejected with correct error
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        concat(df)
        
    # Test that single Series is rejected with correct error  
    with pytest.raises(TypeError, match="first argument must be an iterable"):
        concat(series)
    
    # Test that lists work correctly
    result1 = concat([df, df])
    assert isinstance(result1, DataFrame)
    
    result2 = concat([series, series])
    assert isinstance(result2, pd.Series)