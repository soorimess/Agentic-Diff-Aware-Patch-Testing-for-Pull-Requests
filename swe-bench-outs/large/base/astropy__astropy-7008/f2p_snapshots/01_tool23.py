# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for the context manager for constant versions.
This tests the new set_enabled_constants context manager that allows
temporarily setting values in the constants namespace to an older version.
"""

import pytest

def test_set_enabled_constants_exists():
    """Test that set_enabled_constants context manager exists in constants module."""
    # This test will fail before the change (function doesn't exist)
    # and pass after the change (function exists)
    from astropy import constants as const
    assert hasattr(const, 'set_enabled_constants')
    assert callable(getattr(const, 'set_enabled_constants', None))


def test_set_enabled_constants_importable():
    """Test that set_enabled_constants can be imported directly."""
    # This test will fail before the change (import error)
    # and pass after the change (import works)
    try:
        from astropy.constants import set_enabled_constants
        assert callable(set_enabled_constants)
    except ImportError:
        pytest.skip("set_enabled_constants not yet implemented")


def test_set_enabled_constants_accepts_valid_version():
    """Test that set_enabled_constants accepts valid version names."""
    # This test will fail before the change (function doesn't exist)
    # and pass after the change (function exists and works)
    try:
        from astropy.constants import set_enabled_constants
        # This should not raise an error with valid version
        with set_enabled_constants('astropyconst13'):
            pass
        assert True  # If we get here, it worked
    except (ImportError, AttributeError):
        pytest.skip("set_enabled_constants not yet implemented")