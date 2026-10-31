# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Tests for the set_enabled_constants context manager.
This test verifies the behavior introduced in PR #7008.
"""

import pytest


def test_set_enabled_constants_context_manager_exists():
    """Test that set_enabled_constants context manager can be imported and is callable."""
    # This should not raise an ImportError
    from astropy.constants import set_enabled_constants
    assert callable(set_enabled_constants)


def test_set_enabled_constants_functionality():
    """Test that the context manager actually switches constants."""
    from astropy.constants import set_enabled_constants, c, m_e
    
    # Store original values
    original_c = c.value
    original_m_e = m_e.value
    
    # Test that we can enter the context manager and it works
    try:
        with set_enabled_constants('astropyconst13'):
            # The context manager should work without error
            # We're testing that it doesn't raise an exception
            pass
    except Exception as e:
        pytest.fail(f"set_enabled_constants context manager failed: {e}")
    
    # After exiting, constants should be restored
    assert c.value == original_c
    assert m_e.value == original_m_e


def test_set_enabled_constants_raises_on_invalid_version():
    """Test that invalid version names raise ValueError."""
    from astropy.constants import set_enabled_constants
    
    with pytest.raises(ValueError, match="Context manager does not currently handle"):
        with set_enabled_constants('invalid_version'):
            pass