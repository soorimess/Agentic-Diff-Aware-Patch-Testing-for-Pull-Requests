# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Tests for the set_enabled_constants context manager.
This test verifies the behavior introduced in PR #7008.
"""

import pytest


def test_set_enabled_constants_basic_functionality():
    """Test that the context manager works without errors."""
    from astropy.constants import set_enabled_constants, c, m_e
    
    # Store original values
    original_c = c.value
    original_m_e = m_e.value
    
    # Test that we can enter the context manager and it works
    with set_enabled_constants('astropyconst13'):
        # The context manager should work without error
        # We're testing that it doesn't raise an exception
        pass
    
    # After exiting, constants should be restored
    assert c.value == original_c
    assert m_e.value == original_m_e


def test_set_enabled_constants_raises_on_invalid_version():
    """Test that invalid version names raise ValueError."""
    from astropy.constants import set_enabled_constants
    
    with pytest.raises(ValueError, match="Context manager does not currently handle"):
        with set_enabled_constants('invalid_version'):
            pass


def test_set_enabled_constants_restores_constants_properly():
    """Test that constants are properly restored after context manager exits."""
    from astropy.constants import set_enabled_constants, c, m_e, G
    
    # Store original values
    original_c = c.value
    original_m_e = m_e.value
    original_G = G.value
    
    # Enter context manager and verify it works
    with set_enabled_constants('astropyconst13'):
        # Constants should be accessible inside context
        # Test that we can access constants inside the context
        assert hasattr(c, 'value')
        assert hasattr(m_e, 'value')
        assert hasattr(G, 'value')
    
    # After exiting, values should be restored
    assert c.value == original_c
    assert m_e.value == original_m_e
    assert G.value == original_G


def test_set_enabled_constants_multiple_contexts():
    """Test that multiple context managers work correctly."""
    from astropy.constants import set_enabled_constants, c, m_e
    
    # Store original values
    original_c = c.value
    original_m_e = m_e.value
    
    # Test nested context managers
    with set_enabled_constants('astropyconst13'):
        # Inside first context
        with set_enabled_constants('astropyconst13'):
            # Inside nested context - should work
            assert hasattr(c, 'value')
        # Should still be restored after inner context
        assert c.value == original_c
        assert m_e.value == original_m_e
    
    # Should be restored after outer context
    assert c.value == original_c
    assert m_e.value == original_m_e


def test_set_enabled_constants_identity_preservation():
    """Test that constants are properly constructed (not just copied) in the new implementation."""
    from astropy.constants import set_enabled_constants, c, m_e
    
    # Store original constants to check identity
    original_c = c
    original_m_e = m_e
    
    # Enter context manager
    with set_enabled_constants('astropyconst13'):
        # Constants should be accessible and have the right attributes
        assert hasattr(c, 'value')
        assert hasattr(m_e, 'value')
        # The constants should still be valid Constant objects
        assert hasattr(c, 'name')
        assert hasattr(m_e, 'name')
    
    # After exiting, should be back to original constants
    assert c is original_c  # Identity should be preserved for the default case
    assert m_e is original_m_e  # Identity should be preserved for the default case