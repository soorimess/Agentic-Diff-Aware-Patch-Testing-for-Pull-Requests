# Copyright (c) 2023, 2024 PyCQA and contributors
# SPDX-License-Identifier: GPL-2.0-or-later

"""Test for the bug where min-similarity-lines=0 should disable duplicate code checking."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from pylint.checkers import similar


def test_min_similarity_lines_zero_disables_duplicate_checking() -> None:
    """Test that setting min-similarity-lines to 0 disables duplicate code checking."""
    # Test the actual command line interface behavior
    # When min_lines=0, no duplicate checking should happen
    
    input_path = Path(__file__).parent / "input"
    similar1_path = str(input_path / "similar1")
    similar2_path = str(input_path / "similar2")
    
    # Test with min_lines=0 - should not raise SystemExit because checking is disabled
    output = StringIO()
    with redirect_stdout(output):
        # This should NOT raise SystemExit because min_lines=0 disables checking
        # In the buggy version, it would compute similarities and raise SystemExit
        # In the fixed version, it should return early without computing anything
        try:
            similar.Run(["--duplicates=0", similar1_path, similar2_path])
            # If we get here without exception, that's good - no duplicate checking was done
        except SystemExit:
            # This would be the buggy behavior - it should not happen with min_lines=0
            pytest.fail("Setting --duplicates=0 should disable duplicate checking, but it's still running")


def test_min_similarity_lines_positive_still_works() -> None:
    """Test that setting min-similarity-lines to positive value still enables duplicate checking."""
    # Test the actual command line interface behavior
    # When min_lines > 0, duplicate checking should happen
    
    input_path = Path(__file__).parent / "input"
    similar1_path = str(input_path / "similar1")
    similar2_path = str(input_path / "similar2")
    
    # Test with min_lines=10 - should raise SystemExit because checking is enabled
    # The files have similarities that exceed 10 lines
    output = StringIO()
    with redirect_stdout(output):
        with pytest.raises(SystemExit) as exc_info:
            similar.Run(["--duplicates=10", similar1_path, similar2_path])
        
        # Verify it's the expected exit code for finding duplicates
        assert exc_info.value.code == 0  # Exit code 0 means duplicates found