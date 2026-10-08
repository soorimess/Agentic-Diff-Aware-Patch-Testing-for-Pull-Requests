import pytest
from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_preserves_auth_when_scheme_exists():
    """Test that prepend_scheme_if_needed preserves authentication when scheme already exists."""
    # This should preserve auth even when scheme exists
    # The auth part should be preserved in the netloc
    proxy_url = "http://user:pass@proxy.example.com:8080/path"
    result = prepend_scheme_if_needed(proxy_url, "https")
    # Expected: http://user:pass@proxy.example.com:8080/path (scheme should remain 'http')
    # The auth part should NOT be lost
    assert result == "http://user:pass@proxy.example.com:8080/path"