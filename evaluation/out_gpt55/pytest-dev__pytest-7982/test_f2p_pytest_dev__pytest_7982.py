from _pytest.pathlib import symlink_or_skip


def test_collect_symlinked_directory(testdir):
    target = testdir.tmpdir.dirpath().mkdir("target")
    target.ensure("test_real.py").write("def test_collected(): pass", ensure=True)
    symlink = testdir.tmpdir.join("symlink")
    symlink_or_skip(target, symlink, target_is_directory=True)

    result = testdir.runpytest("-v")

    result.stdout.fnmatch_lines(["symlink/test_real.py::test_collected PASSED*"])
    assert result.ret == 0
