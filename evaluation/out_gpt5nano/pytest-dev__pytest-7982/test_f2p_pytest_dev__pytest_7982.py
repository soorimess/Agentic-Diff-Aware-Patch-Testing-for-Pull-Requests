import os
import pytest

from _pytest.pytester import Pytester


def test_symlink_directory_collection_obs(pytester: Pytester) -> None:
    # Setup: create a real directory with a simple test file and a symlink to it
    root = pytester.path
    target = root.joinpath("target_dir_for_symlink")
    target.mkdir()
    (target / "test_inside.py").write_text(
        "def test_inside():\n    assert True\n", encoding="utf-8"
    )

    link = root.joinpath("link_to_target_dir_symlink")
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink creation not supported in this environment: {exc!r}")

    # Run pytest only on the symlink path.
    # Pre-commit (old) code should skip following symlinks, collecting 0 items from the symlink dir.
    # The patch (post-commit) should follow the symlink and collect the test inside.
    result = pytester.runpytest("-q", str(link))
    out = result.stdout.str()
    assert "collected 1 item" in out or "collected 1 items" in out
