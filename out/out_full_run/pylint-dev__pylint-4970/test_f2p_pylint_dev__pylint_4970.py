# Regression test for behavior described in https://github.com/PyCQA/pylint/issues/4970
# Ensures that setting min-similarity-lines (duplicates) to 0 disables duplicate code checks
# as observed by Similar.Run: when duplicates=0 the similarity runner should not print a report.
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from pylint.checkers import similar


def test_min_similarity_lines_zero_stops_reporting(tmp_path: Path) -> None:
    # Create two files with identical code so duplicates would normally be detected
    content = """def example():
    x = 1
    y = x + 2
    return y
"""
    f1 = tmp_path / "f1.py"
    f2 = tmp_path / "f2.py"
    f1.write_text(content)
    f2.write_text(content)

    out = StringIO()
    # similar.Run exits with SystemExit; capture stdout and the exit
    with redirect_stdout(out), pytest.raises(SystemExit) as exc:
        similar.Run(["--duplicates", "0", str(f1), str(f2)])
    assert exc.value.code == 0
    output = out.getvalue()
    # After the fix, --duplicates 0 should disable similarity checking and produce no report
    assert output.strip() == ""
