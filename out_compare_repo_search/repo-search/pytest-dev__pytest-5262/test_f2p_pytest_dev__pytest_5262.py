from _pytest.capture import EncodedFile


def test_encodedfile_mode_does_not_include_b():
    class DummyBuffer:
        def __init__(self):
            self.mode = "rb+"
            self.encoding = "utf-8"
            self.written = []

        def write(self, obj):
            self.written.append(obj)

    buf = DummyBuffer()
    ef = EncodedFile(buf, "utf-8")
    # The EncodedFile.mode property should not advertise binary mode (no 'b').
    # Before the fix this returned the underlying buffer.mode (e.g. 'rb+')
    # which caused external libraries to think they should write bytes.
    assert "b" not in ef.mode
