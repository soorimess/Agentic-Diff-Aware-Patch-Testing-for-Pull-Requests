# -*- coding: utf-8 -*-

import pytest
from requests.utils import prepend_scheme_if_needed


class TestPrependSchemeWithAuth:
    """Test that prepend_scheme_if_needed preserves authentication in URLs."""

    def test_preserves_auth_when_scheme_exists(self):
        """Test that authentication info is preserved when URL already has a scheme."""
        # This is the core bug: auth should be preserved even when scheme exists
        url_with_auth = "http://user:pass@example.com/path"
        result = prepend_scheme_if_needed(url_with_auth, "https")
        # The scheme should NOT be changed (docstring says "Does not replace a present scheme")
        # But auth should be preserved
        expected = "http://user:pass@example.com/path"
        assert result == expected

    def test_preserves_auth_with_port(self):
        """Test that authentication info is preserved with port numbers."""
        url_with_auth_and_port = "http://user:pass@example.com:8080/path"
        result = prepend_scheme_if_needed(url_with_auth_and_port, "https")
        expected = "http://user:pass@example.com:8080/path"
        assert result == expected

    def test_prepends_scheme_when_none_exists(self):
        """Test that scheme is properly prepended when none exists."""
        url_without_scheme = "example.com/path"
        result = prepend_scheme_if_needed(url_without_scheme, "https")
        expected = "https://example.com/path"
        assert result == expected

    def test_auth_with_query_and_fragment(self):
        """Test that authentication works with query parameters and fragments."""
        url_with_auth_query_fragment = "http://user:pass@example.com/path?query=value#fragment"
        result = prepend_scheme_if_needed(url_with_auth_query_fragment, "https")
        expected = "http://user:pass@example.com/path?query=value#fragment"
        assert result == expected

    def test_no_auth_still_works(self):
        """Test that URLs without auth still work as before."""
        url_without_auth = "http://example.com/path"
        result = prepend_scheme_if_needed(url_without_auth, "https")
        expected = "http://example.com/path"
        assert result == expected