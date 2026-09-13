import pytest
from _pytest.capture import EncodedFile


def test_encodedfile_mode_does_not_advertise_binary(tmp_path):
    """EncodedFile.mode should not include the binary 'b' flag.

    Some third-party libraries decide whether to write bytes or text
    by checking for 'b' in the destination stream's mode. EncodedFile
    must therefore not advertise a 'b' in its mode, even if the
    underlying buffer is a binary file descriptor.
    """
    p = tmp_path / "f"
    # open a binary-backed file so the underlying buffer.mode contains 'b'
    f = open(str(p), "wb+")
    try:
        enc = EncodedFile(f, encoding="utf8")
        assert "b" not in enc.mode
    finally:
        f.close()
