# Copyright (c) 2021, 2022, 2023, 2024 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021, 2022, 2023, 2024 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2021, 2022, 2023, 2024 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021, 2022, 2023, 2024 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Regression test for min-similarity-lines = 0 disabling duplicate code checking"""

from unittest.mock import patch, MagicMock
from pylint.checkers import similar


def test_min_similarity_lines_zero_returns_early():
    """
    Test that when SimilarChecker is initialized with min_lines=0,
    the run() method returns early without doing any similarity processing.
    
    Before fix: SimilarChecker.run() would process similarity detection even when min_lines=0
    After fix: SimilarChecker.run() returns early when min_lines=0  
    """
    # Create a SimilarChecker with min_lines=0
    checker = similar.SimilarChecker(None)
    checker.min_lines = 0
    
    # Mock the methods that would be called to verify the early return
    with patch.object(checker, '_compute_sims') as mock_compute, \
         patch.object(checker, '_display_sims') as mock_display:
        
        # Create a mock that doesn't actually do computation
        mock_compute.return_value = []
        
        # Call run - this should return early due to min_lines=0
        checker.run()
        
        # If the bug is present (old behavior), _compute_sims and _display_sims would be called
        # If the fix is in place (new behavior), they should never be called
        assert not mock_compute.called, "With min_lines=0, _compute_sims should not be called"
        assert not mock_display.called, "With min_lines=0, _display_sims should not be called"


def test_min_similarity_lines_positive_processes():
    """
    Test that when SimilarChecker is initialized with min_lines>0,
    the run() method processes similarities normally.
    
    This validates that normal functionality is not broken.
    """
    # Create a SimilarChecker with min_lines=4 (normal case)
    checker = similar.SimilarChecker(None)
    checker.min_lines = 4
    
    # Mock the methods to verify they get called
    with patch.object(checker, '_compute_sims') as mock_compute, \
         patch.object(checker, '_display_sims') as mock_display:
        
        # Set up mocks to return some test data
        mock_compute.return_value = [("test", {1, 2, 3})]
        
        # Call run - this should proceed normally
        checker.run()
        
        # These should be called because min_lines > 0
        assert mock_compute.called, "With min_lines>0, _compute_sims should be called"
        assert mock_display.called, "With min_lines>0, _display_sims should be called"