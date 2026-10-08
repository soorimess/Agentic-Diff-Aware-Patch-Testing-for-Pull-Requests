# -*- coding: utf-8 -*-
"""
Regression test for proxy authentication bug in requests library.

This test ensures that when a URL with authentication is processed by
prepend_scheme_if_needed, the authentication information is properly preserved.
"""

import pytest
from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_preserves_auth_when_scheme_exists():
    """Test that authentication info is preserved when URL already has a scheme."""
    # This is the key case that was broken - URLs with auth that already have schemes
    url_with_auth = "http://user:pass@example.com"
    result = prepend_scheme_if_needed(url_with_auth, "https")
    # The auth should be preserved in the netloc even though scheme is not changed
    # The auth should be in the format "user:pass@example.com"
    assert result == "http://user:pass@example.com"


def test_prepend_scheme_if_needed_preserves_auth_with_path():
    """Test that authentication info is preserved when URL with auth and path."""
    url_with_auth = "http://user:pass@example.com/path/to/resource"
    result = prepend_scheme_if_needed(url_with_auth, "https")
    # The auth should be preserved in the netloc
    assert result == "http://user:pass@example.com/path/to/resource"


def test_prepend_scheme_if_needed_preserves_auth_with_port():
    """Test that authentication info is preserved when URL with auth and port."""
    url_with_auth = "http://user:pass@example.com:8080"
    result = prepend_scheme_if_needed(url_with_auth, "https")
    # The auth should be preserved in the netloc
    assert result == "http://user:pass@example.com:8080"


def test_prepend_scheme_if_needed_preserves_auth_with_port_and_path():
    """Test that authentication info is preserved when URL with auth, port and path."""
    url_with_auth = "http://user:pass@example.com:8080/path/to/resource"
    result = prepend_scheme_if_needed(url_with_auth, "https")
    # The auth should be preserved in the netloc
    assert result == "http://user:pass@example.com:8080/path/to/resource"


def test_prepend_scheme_if_needed_without_auth_still_works():
    """Test that URLs without authentication still work as before."""
    url_without_auth = "example.com"
    result = prepend_scheme_if_needed(url_without_auth, "https")
    expected = "https://example.com"
    assert result == expected


def test_prepend_scheme_if_needed_without_auth_with_path():
    """Test that URLs without authentication with path still work as before."""
    url_without_auth = "example.com/path"
    result = prepend_scheme_if_needed(url_without_auth, "https")
    expected = "https://example.com/path"
    assert result == expected


def test_prepend_scheme_if_needed_already_has_scheme_no_change():
    """Test that when URL already has scheme, it doesn't get changed (per docstring)."""
    # This test verifies the documented behavior that existing schemes are not replaced
    url_with_scheme = "http://example.com"
    result = prepend_scheme_if_needed(url_with_scheme, "https")
    # Should keep the original scheme, not change it
    assert result.startswith("http://")