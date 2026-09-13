from requests.utils import prepend_scheme_if_needed


def test_prepend_scheme_if_needed_preserves_auth_with_scheme():
    url = 'http://user:pass@example.com/path?a=1#test'
    # The username:password should be preserved when prepending a scheme.
    assert prepend_scheme_if_needed(url, 'http') == url
