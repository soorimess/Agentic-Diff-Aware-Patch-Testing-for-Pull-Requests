import requests


def test_get_and_head_do_not_send_content_length_by_default():
    """GET and HEAD requests should not include a Content-Length header when
    there is no body. This would cause some servers to reject the request.
    """
    for method in ("GET", "HEAD"):
        req = requests.Request(method, 'http://example.com')
        prepped = req.prepare()
        assert 'Content-Length' not in prepped.headers

    # Non GET/HEAD methods without a body should still send Content-Length: 0
    req = requests.Request('POST', 'http://example.com')
    prepped = req.prepare()
    assert prepped.headers.get('Content-Length') == '0'
