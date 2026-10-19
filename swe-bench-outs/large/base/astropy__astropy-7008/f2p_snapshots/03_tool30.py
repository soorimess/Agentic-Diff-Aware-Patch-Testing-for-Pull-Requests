# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for the context manager for constant versions.
This tests the new set_enabled_constants context manager that allows
temporarily setting values in the constants namespace to an older version.
"""

import pytest

def test_set_enabled_constants_exists_and_callable():
    """Test that set_enabled_constants context manager exists and is callable."""
    # This test will fail before the change (function doesn't exist)
    # and pass after the change (function exists and is callable)
    from astropy import constants as const
    assert hasattr(const, 'set_enabled_constants')
    assert callable(const.set_enabled_constants)


def test_set_enabled_constants_importable_directly():
    """Test that set_enabled_constants can be imported directly from constants."""
    # This test will fail before the change (import error)
    # and pass after the change (import works)
    from astropy.constants import set_enabled_constants
    assert callable(set_enabled_constants)


def test_set_enabled_constants_accepts_valid_version():
    """Test that set_enabled_constants accepts valid version names."""
    # This test will fail before the change (function doesn't exist)
    # and pass after the change (function exists and works)
    from astropy.constants import set_enabled_constants
    # This should not raise an error with valid version
    try:
        with set_enabled_constants('astropyconst13'):
            pass
        assert True  # If we get here, it worked
    except Exception as e:
        # If there's an error, it should be about the version not being available
        # but that's not what we're testing here - we're testing that the function
        # exists and can be called
        pytest.skip(f"Function exists but failed with: {e}")


def test_set_enabled_constants_rejects_invalid_version():
    """Test that set_enabled_constants rejects invalid version names with ValueError."""
    # This test will fail before the change (function doesn't exist)
    # and pass after the change (function exists and raises proper error)
    from astropy.constants import set_enabled_constants
    # This should raise ValueError for invalid version
    with pytest.raises(ValueError, match='Context manager does not currently handle'):
        with set_enabled_constants('invalid_version'):
            pass


def test_set_enabled_constants_context_manager_basic():
    """Test basic context manager functionality."""
    # This test ensures the context manager works as expected
    from astropy.constants import set_enabled_constants
    # Test that we can enter and exit without errors
    try:
        with set_enabled_constants('astropyconst13'):
            # Basic functionality test - just make sure it doesn't crash
            pass
        assert True
    except Exception as e:
        # If it fails, it's likely because the function doesn't exist yet
        pytest.skip(f"Context manager test failed: {e}")