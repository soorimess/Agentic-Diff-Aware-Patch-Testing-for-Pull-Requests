from __future__ import absolute_import, division, print_function

import tempfile

import _pytest.capture as capture


def test_encodedfile_mode_is_text_mode():
    """EncodedFile.mode should not advertise binary ('b') in its mode.

    Some libraries (eg youtube-dl) check for 'b' in file.mode to decide
    whether to write bytes or text. EncodedFile wraps a binary buffer but
    should present a text-mode-like .mode to callers so they choose to
    write text (str) rather than bytes.
    """
    f = tempfile.TemporaryFile()
    ef = capture.EncodedFile(f, "utf-8")
    assert "b" not in ef.mode
