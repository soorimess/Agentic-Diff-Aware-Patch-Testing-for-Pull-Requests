"""Regression test for issue pylint-dev/pylint#4970

Setting `min-similarity-lines` (duplicates) to 0 should disable the
similarity/duplication checker. When run as the standalone similarities tool
this means it should produce no output when --duplicates 0 is used.

This reproduces the behaviour before the fix where the tool still printed a
TOTAL report even when the threshold was 0.
"""
from contextlib import redirect_stdout
from io import StringIO

import pytest

from pylint.checkers import similar


def test_similar_run_with_duplicates_zero_emits_no_output() -> None:
    """When duplicates/`min-similarity-lines` is set to 0 the tool should do nothing.

    The standalone runner similar.Run takes a ``--duplicates`` / ``-d``
    argument and exits with SystemExit(0). Prior to the fix it still
    printed a report (TOTAL lines=... duplicates=0). The desired behaviour
    is to suppress any output when the feature is disabled with 0.
    """
    output = StringIO()
    # Use two input files that normally would be scanned for similarities.
    args = ["--duplicates", "0", "tests/input/similar1", "tests/input/similar2"]
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(args)
    # Run should exit cleanly
    assert ex.value.code == 0
    # With duplicates disabled there should be no output at all
    assert output.getvalue().strip() == ""
