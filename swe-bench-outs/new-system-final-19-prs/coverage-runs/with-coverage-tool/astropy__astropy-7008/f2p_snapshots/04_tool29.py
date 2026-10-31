# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for the context manager for constant versions.
"""

import pytest


def test_set_enabled_constants_context_manager_exists():
    """Test that the context manager exists and can be imported."""
    # Import the function to make sure it's available
    from astropy.constants import set_enabled_constants
    # Test that it's actually a callable context manager
    assert callable(set_enabled_constants)


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


def test_constants_import_and_functionality():
    """Test that constants are properly set up and available after importing astropyconst20."""
    # Import astropyconst20 to make sure it works with new _set_c approach
    import astropy.constants.astropyconst20
    
    # Test that constants are accessible
    from astropy.constants import c, h
    assert c is not None
    assert h is not None
    
    # Test that the astropyconst20 module can be imported and has constants
    assert hasattr(astropy.constants.astropyconst20, 'c')
    assert hasattr(astropy.constants.astropyconst20, 'h')