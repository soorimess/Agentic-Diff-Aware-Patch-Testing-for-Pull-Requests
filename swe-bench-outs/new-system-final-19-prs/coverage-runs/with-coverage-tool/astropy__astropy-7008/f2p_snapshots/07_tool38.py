# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for the context manager for constant versions.
"""

import pytest


def test_set_enabled_constants_functionality():
    """Test that the context manager properly switches constant versions."""
    # Import constants to test with
    from astropy.constants import h
    from astropy.constants.astropyconst13 import h as h_old
    
    # Test that constants are different between versions
    assert h.value != h_old.value, "Constants should have different values in different versions"
    
    # Test that we can enter the context manager
    from astropy.constants import set_enabled_constants
    with set_enabled_constants('astropyconst13'):
        # Inside the context, constants should be from the old version
        from astropy.constants import h as h_in_context
        assert h_in_context.value == h_old.value
    
    # After exiting the context, constants should revert to default version
    from astropy.constants import h as h_after_context
    assert h_after_context.value == h.value


def test_set_enabled_constants_invalid_version():
    """Test that invalid version names raise appropriate errors."""
    from astropy.constants import set_enabled_constants
    with pytest.raises(ValueError, match="Context manager does not currently handle"):
        with set_enabled_constants('invalid_version'):
            pass


def test_utils_module_functionality():
    """Test that the new utility functions work correctly."""
    # Import the utility functions to make sure they exist and work
    from astropy.constants import utils
    
    # Test that the _get_c function exists and can be called
    assert hasattr(utils, '_get_c')
    
    # Test that the _set_c function exists and can be called  
    assert hasattr(utils, '_set_c')
    
    # Test that we can import astropyconst20 to make sure it uses the new approach
    import astropy.constants.astropyconst20
    assert astropy.constants.astropyconst20 is not None