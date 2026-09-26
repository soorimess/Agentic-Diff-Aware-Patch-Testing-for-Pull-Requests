# Copyright (c) 2021-2023, 2024 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2021-2023, 2024 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021-2023, 2024 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021-2023, 2024 Hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021-2023, 2024 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2021-2023, 2024 Eli Fine <ejfine@gmail.com>
# Copyright (c) 2021-2023, 2024 Maksym Humetskyi <Humetsky@gmail.com>
# Copyright (c) 2021-2023, 2024 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021-2023, 2024 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021-2023, 2024 Aditya Gupta <adityagupta1089@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Regression test for issue #4970 - Setting min-similarity-lines to 0 should disable checking for duplicate code."""

import tempfile
import os
from unittest.mock import patch

from pylint.checkers import similar
from pylint.lint import PyLinter


def test_min_similarity_lines_zero_returns_early():
    """
    Test that when min-similarity-lines is set to 0, the run method returns early
    without executing the duplicate checking algorithm.
    
    This test specifically checks that the early return behavior is working by
    ensuring that the duplicate checking methods are not called when min_lines=0.
    """
    
    # Create test content
    test_content = """
def helper():
    return 42

def another_helper():
    return 42
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Create linter and checker
        linter = PyLinter()
        checker = similar.SimilarChecker(linter)
        
        # Configure to disable duplicate checking
        checker.set_option('min-similarity-lines', 0)
        
        # Add file to checker
        with open(temp_file, 'r') as stream:
            checker.append_stream(temp_file, stream)
        
        # Mock the methods that would be called if duplicate checking ran
        # This test verifies that these methods are NOT called when min_lines=0
        with patch.object(checker, '_compute_sims') as mock_compute, \
             patch.object(checker, '_display_sims') as mock_display:
            
            # Run the checker - this should return early without calling the duplicate checking methods
            checker.run()
            
            # Verify that the duplicate checking methods were NOT called
            # This is the key assertion that would fail if the fix wasn't in place
            mock_compute.assert_not_called()
            mock_display.assert_not_called()
        
        # If we get here without error, the fix is working correctly
        # The early return prevents execution of duplicate checking algorithms
        
    finally:
        os.unlink(temp_file)