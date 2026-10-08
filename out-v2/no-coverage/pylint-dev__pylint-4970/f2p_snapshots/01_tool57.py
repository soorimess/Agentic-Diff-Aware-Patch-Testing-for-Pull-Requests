# Copyright (c) 2021, 2022 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021, 2022 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2021, 2022 Ashley Whetter <ashley@awhetter.co.uk>

# Licensed under the GPL: https://www.gnu.org/licenses/old-loses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Regression test for issue #4970 - Setting `min-similarity-lines` to `0` should disable checking for duplicate code."""

from io import StringIO
from unittest.mock import patch
from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter


def test_min_similarity_lines_zero_returns_early():
    """Test that SimilarChecker.run() returns early when min_lines=0 to disable duplicate checking."""
    
    # Create a linter with reporter
    linter = PyLinter(reporter=Reporter())
    
    # Create SimilarChecker with min_lines=0 (should disable duplicate checking)
    checker = similar.SimilarChecker(linter)
    checker.min_lines = 0
    
    # Add test content that would trigger duplicate warnings if not disabled
    content1 = "x = 1\ny = 2\n"
    content2 = "x = 1\ny = 2\n"
    
    with StringIO(content1) as stream1:
        checker.append_stream("file1.py", stream1)
    
    with StringIO(content2) as stream2:
        checker.append_stream("file2.py", stream2)
    
    # Mock _compute_sims to see if it gets called
    with patch.object(checker, '_compute_sims') as mock_compute:
        mock_compute.return_value = []
        
        # This should complete without calling _compute_sims when min_lines=0
        checker.run()
        
        # If the fix is working, _compute_sims should NOT be called
        # If the bug exists, _compute_sims would be called
        assert not mock_compute.called, "When min_lines=0, _compute_sims should not be called"