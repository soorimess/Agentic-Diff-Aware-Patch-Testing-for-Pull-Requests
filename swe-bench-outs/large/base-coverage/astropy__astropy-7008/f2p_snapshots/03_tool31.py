# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Tests for the context manager for constant versions.
"""

import pytest


def test_set_enabled_constants_context_manager_exists():
    """Test that the context manager exists and can be imported."""
    from astropy.constants import set_enabled_constants
    assert set_enabled_constants is not None


def test_set_enabled_constants_only_accepts_supported_versions():
    """Test that the context manager only accepts supported versions."""
    from astropy.constants import set_enabled_constants
    
    # This should raise ValueError for unsupported version
    with pytest.raises(ValueError, match="Context manager does not currently handle"):
        with set_enabled_constants('nonexistent_version'):
            pass


def test_set_enabled_constants_error_message_contains_version():
    """Test that error message contains the version name."""
    from astropy.constants import set_enabled_constants
    
    # Test that error message mentions the version being rejected
    with pytest.raises(ValueError, match="nonexistent_version"):
        with set_enabled_constants('nonexistent_version'):
            pass


def test_set_enabled_constants_works_with_supported_version():
    """Test that the context manager works with supported version."""
    from astropy.constants import set_enabled_constants
    
    # This should not raise an exception for supported version
    try:
        with set_enabled_constants('astropyconst13'):
            # Just test that we can enter and exit without error
            pass
        assert True  # If we get here, it worked
    except Exception as e:
        pytest.fail(f"set_enabled_constants('astropyconst13') raised {type(e).__name__}: {e}")