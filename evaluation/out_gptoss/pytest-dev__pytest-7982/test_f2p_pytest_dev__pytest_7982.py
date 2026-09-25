"""Regression test for bug #7982: symlinked directories not collected.

This test ensures that symlinked directories inside a test directory are properly
followed and their test files collected. The buggy implementation skipped symlinks
and missed tests. The change removes follow_symlinks=False from visit to fix it.
"""

from _pytest.pathlib import symlink_or_skip


def test_symlinked_subdirectory_collection(testdir):
    """A symlinked directory inside a test directory should be collected."""
    # Create a real directory containing a test file.
    real_dir = testdir.mkdir("real")
    real_dir.join("test_x.py").write("def test_x(): pass")

    # Create a parent directory to host the symlink.
    root_dir = testdir.mkdir("root")
    symlink_dir = root_dir.join("symlink")
    symlink_or_skip(real_dir, symlink_dir, target_is_directory=True)

    # Run pytest on the parent directory.
    result = testdir.runpytest('-v', str(root_dir))

    # Expect the test from the symlinked directory to be collected.
    result.stdout.fnmatch_lines(["root/symlink/test_x.py::test_x PASSED*"])
    assert result.ret == 0
