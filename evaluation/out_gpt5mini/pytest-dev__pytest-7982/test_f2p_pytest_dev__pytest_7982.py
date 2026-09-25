import textwrap

from _pytest.pathlib import symlink_or_skip


def test_follow_symlinked_directory_is_collected(testdir):
    """A symlink to a directory inside a testroot should be followed and collected.

    Regression test for pytest-dev/pytest#7982: visit(...).is_dir(follow_symlinks=False)
    caused symlinked directories to be skipped during collection.
    """
    # Create a real directory containing a test file
    real = testdir.mkdir("real_tests")
    real.join("test_real.py").write(textwrap.dedent("""
        def test_in_real():
            assert True
    """))

    # Create a root directory and a symlink inside it that points to the real directory
    root = testdir.mkdir("root")
    symlink = root.join("link_to_real")
    # On platforms that don't support symlinks this will skip the test
    symlink_or_skip(real, symlink, target_is_directory=True)

    # Running pytest on the root should discover the test inside the symlinked directory
    result = testdir.runpytest(str(root))
    # We expect the test from the symlinked directory to be collected and to pass
    result.stdout.fnmatch_lines(["*1 passed in*"])
    assert result.ret == 0
