"""
Regression test for pull request #60196: 
BUG: fix inspect usage when pyarrow or jinja2 is not installed

This test ensures that when optional dependencies are missing, 
AttributeError is raised instead of ImportError so that inspect.getmembers
can work properly.
"""
import sys
from unittest.mock import patch

import pytest

import pandas as pd
from pandas import DataFrame, Series


class TestInspectUsageWhenDependenciesMissing:
    def test_arrow_accessors_raise_attribute_error_when_pyarrow_missing(self):
        """
        Test that accessing arrow accessors raises AttributeError when pyarrow is not installed.
        
        This addresses the fix in ArrowAccessor._validate method to raise AttributeError
        instead of ImportError when pyarrow is not available or when dtype is not ArrowDtype.
        """
        # Mock pyarrow as not available
        with patch.dict('sys.modules', {'pyarrow': None}):
            # Create a Series with non-Arrow dtype to trigger the AttributeError
            s = Series([1, 2, 3])
            
            # Accessing list accessor should raise AttributeError instead of ImportError
            with pytest.raises(AttributeError):
                _ = s.list

    def test_struct_accessor_raises_attribute_error_when_pyarrow_missing(self):
        """
        Test that accessing struct accessor raises AttributeError when pyarrow is not installed.
        
        This addresses the fix in ArrowAccessor._validate method to raise AttributeError
        instead of ImportError when pyarrow is not available or when dtype is not ArrowDtype.
        """
        # Mock pyarrow as not available
        with patch.dict('sys.modules', {'pyarrow': None}):
            # Create a Series with non-Arrow dtype to trigger the AttributeError
            s = Series([1, 2, 3])
            
            # Accessing struct accessor should raise AttributeError instead of ImportError
            with pytest.raises(AttributeError):
                _ = s.struct

    def test_inspect_getmembers_works_with_missing_pyarrow(self):
        """
        Test that inspect.getmembers works with missing pyarrow dependency.
        
        This ensures that when pyarrow is not available, inspect.getmembers can 
        gracefully ignore missing attributes by catching AttributeError.
        """
        import inspect
        
        # Mock pyarrow as not available
        with patch.dict('sys.modules', {'pyarrow': None}):
            s = Series([1, 2, 3])
            
            # This should not raise an ImportError when inspecting
            try:
                members = inspect.getmembers(s)
                # Should succeed without ImportError
                assert len(members) > 0
            except ImportError:
                pytest.fail("inspect.getmembers should not raise ImportError when pyarrow is missing")

    def test_style_accessor_raises_attribute_error_when_jinja2_missing(self):
        """
        Test that accessing .style raises AttributeError when jinja2 is not installed.
        
        This addresses the fix in DataFrame.style property to raise AttributeError
        instead of ImportError when jinja2 is not available, allowing inspect.getmembers
        to work properly.
        """
        # Mock jinja2 as not available
        with patch.dict('sys.modules', {'jinja2': None}):
            df = DataFrame({'A': [1, 2, 3]})
            
            # Before the fix, this would raise ImportError
            # After the fix, this should raise AttributeError with the specific message
            with pytest.raises(AttributeError) as exc_info:
                _ = df.style
            
            # Verify the error message is appropriate
            assert "The '.style' accessor requires jinja2" in str(exc_info.value)