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


def test_astropyconst20_module_functionality():
    """Test that astropyconst20 module works correctly with new _set_c approach."""
    # Import astropyconst20 to make sure it works with the new approach
    import astropy.constants.astropyconst20
    
    # Test that we can access constants from the module
    # This exercises the module-level code that was changed
    c20 = astropy.constants.astropyconst20.c
    h20 = astropy.constants.astropyconst20.h
    
    # Verify they are actual constants
    assert hasattr(c20, 'value')
    assert hasattr(h20, 'value')
    
    # Test that we can also access them through the main constants module
    from astropy.constants import c, h
    assert c is not None
    assert h is not None
    
    # Test that the values are accessible
    assert c20.value is not None
    assert h20.value is not None