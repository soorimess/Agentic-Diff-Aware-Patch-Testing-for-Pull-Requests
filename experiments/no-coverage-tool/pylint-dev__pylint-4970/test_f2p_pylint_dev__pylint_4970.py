# Copyright (c) 2022, 2023 PyCQA
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Regression test for the bug where min-similarity-lines=0 should disable
duplicate code checking but instead treats all code as similar.

This test specifically ensures the fix that adds early return when min_lines=0 works.
"""

import unittest.mock as mock
from pathlib import Path
from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter


def test_min_similarity_zero_prevents_similarity_computation():
    """
    Test to ensure setting min-similarity-lines to 0 prevents similarity computation.
    
    Before fix: run() always calls _compute_sims() even when min_lines=0
    After fix: run() returns early without calling _compute_sims() when min_lines=0
    """
    
    # Setup simple files
    test_file = Path("temp_test.py")
    test_file.write_text("def a(): pass\n\ndef b(): pass\n")
    
    try:
        # Setup linter
        linter = PyLinter()
        reporter = Reporter()
        linter.set_reporter(reporter)
        linter.config.min_similar_lines = 0  # Key setting that should disable checking
        
        checker = similar.SimilarChecker(linter)
        
        # Add file 
        with open(test_file, encoding="utf-8") as stream:
            checker.append_stream(str(test_file), stream)
            
        # The crucial behavior test:
        # When min_lines=0, we want to verify that _compute_sims() is NOT called
        # We test this by mocking and asserting it should NOT be called
        
        with mock.patch.object(checker, '_compute_sims', return_value=[]) as mock_compute:
            # This trigger the code path we're specifically testing
            checker.run()
            
            # After fix, this should NOT be called (early return)
            # Before fix, this would be called (which is the bug)
            mock_compute.assert_not_called()
            
    finally:
        if test_file.exists():
            test_file.unlink()