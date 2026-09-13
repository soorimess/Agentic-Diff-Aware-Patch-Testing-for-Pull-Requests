# regression test for issue psf/requests#1142
# ensure GET requests do not send a Content-Length header

import requests


def test_get_should_not_send_content_length_header():
    """A prepared GET request with no body must not include Content-Length.

    The project previously always added a Content-Length: 0 header to
    requests with no body (including GET/HEAD). This test asserts the
    correct behavior: GET requests without a body must not send
    Content-Length.
    """
    req = requests.Request('GET', 'http://example.com')
    prepped = req.prepare()

    # Case-insensitive header dict; membership checks should work.
    assert 'Content-Length' not in prepped.headers
