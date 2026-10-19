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


def test_set_enabled_constants_accepts_astropyconst13():
    """Test that the context manager accepts the astropyconst13 version."""
    from astropy.constants import set_enabled_constants
    
    # This should work without raising an exception
    try:
        with set_enabled_constants('astropyconst13'):
            # Just test that we can enter and exit without error
            pass
        assert True  # If we get here, it worked
    except Exception as e:
        pytest.fail(f"set_enabled_constants('astropyconst13') raised {type(e).__name__}: {e}")


def test_set_enabled_constants_error_message_includes_version():
    """Test that error message contains the version name."""
    from astropy.constants import set_enabled_constants
    
    # Test that error message mentions the specific version being rejected
    try:
        with set_enabled_constants('nonexistent_version'):
            pass
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert 'nonexistent_version' in str(e)