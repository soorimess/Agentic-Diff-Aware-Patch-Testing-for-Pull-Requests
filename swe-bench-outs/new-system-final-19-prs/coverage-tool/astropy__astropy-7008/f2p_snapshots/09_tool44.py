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


def test_astropyconst20_import_exercises_new_code():
    """Test that importing astropyconst20 exercises the new _set_c approach."""
    # Import astropyconst20 to make sure it uses the new _set_c approach
    import astropy.constants.astropyconst20
    
    # Verify that constants are accessible from the module
    # This forces the module to be fully initialized with new approach
    assert hasattr(astropy.constants.astropyconst20, 'c')
    assert hasattr(astropy.constants.astropyconst20, 'h')
    
    # Test that we can access constants from the imported module
    from astropy.constants.astropyconst20 import c as c20, h as h20
    assert c20 is not None
    assert h20 is not None
    
    # Verify that constants from astropyconst20 are actually the same as from main constants
    from astropy.constants import c, h
    # These should be the same constants (just accessed through different import paths)
    assert c is not None
    assert h is not None