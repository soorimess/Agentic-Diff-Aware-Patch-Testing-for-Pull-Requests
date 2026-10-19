# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for the context manager for constant versions.
This tests the new set_enabled_constants context manager that allows
temporarily setting values in the constants namespace to an older version.
"""

import pytest

def test_set_enabled_constants_exists_and_callable():
    """Test that set_enabled_constants context manager exists and is callable."""
    from astropy import constants as const
    assert hasattr(const, 'set_enabled_constants')
    assert callable(const.set_enabled_constants)


def test_set_enabled_constants_importable():
    """Test that set_enabled_constants can be imported directly."""
    from astropy.constants import set_enabled_constants
    assert callable(set_enabled_constants)


def test_set_enabled_constants_accepts_valid_version():
    """Test that set_enabled_constants accepts valid version names."""
    from astropy.constants import set_enabled_constants
    # This should not raise an error with valid version
    with set_enabled_constants('astropyconst13'):
        # Basic functionality test - just make sure it doesn't crash
        pass


def test_set_enabled_constants_rejects_invalid_version():
    """Test that set_enabled_constants rejects invalid version names with ValueError."""
    from astropy.constants import set_enabled_constants
    # This should raise ValueError for invalid version
    with pytest.raises(ValueError, match='Context manager does not currently handle'):
        with set_enabled_constants('invalid_version'):
            pass