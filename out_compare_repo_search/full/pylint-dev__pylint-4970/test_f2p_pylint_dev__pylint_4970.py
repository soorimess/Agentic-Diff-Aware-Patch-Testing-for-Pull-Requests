"""Regression test for issue pylint-dev/pylint#4970

Setting min-similarity-lines to 0 should disable duplicate-code checking.
This ensures that calling the similarities CLI with --duplicates 0 produces no
output (the check is effectively turned off) and exits cleanly.

The repository contained a bug where setting this value to 0 caused the
similarity checker to treat every line as duplicate. The correct behaviour is
that the check is skipped.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from pylint.checkers import similar

INPUT = Path(__file__).parent / "input"
SIMILAR1 = str(INPUT / "similar1")
SIMILAR2 = str(INPUT / "similar2")


def test_min_similarity_zero_disables_duplicate_check() -> None:
    """When --duplicates 0 is passed, the similarities check is disabled.

    The CLI entrypoint exits with code 0 and prints nothing to stdout.
    """
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(["--duplicates", "0", SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == ""
