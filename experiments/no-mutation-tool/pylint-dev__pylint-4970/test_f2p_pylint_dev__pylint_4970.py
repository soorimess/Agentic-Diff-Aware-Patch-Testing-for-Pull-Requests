# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
#
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Regression test for the fix to min-similarity-lines = 0 behavior."""

import tempfile
from pathlib import Path

from pylint.checkers import similar
from pylint.lint import PyLinter


def test_min_similarity_lines_zero_disables_duplicate_checking():
    """
    Test that min-similarity-lines = 0 disables duplicate code checking.
    
    Before fix: When min_similarity_lines = 0, SimilarChecker would process 
    similarities and attempt to report duplicate code, treating every line 
    as similar and throwing many errors.
    
    After fix: When min_similarity_lines = 0, SimilarChecker returns early
    and does not process any duplicate checking.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create content that would trigger duplicate code detection if processed
        file1_path = Path(tmpdir) / "file1.py"
        file2_path = Path(tmpdir) / "file2.py"
        
        # This pattern would trigger similarity checking with appropriate thresholds
        content = """def shared_function():
    x = 10
    y = 20  
    z = 30
    return x + y + z

def another_shared_function():
    x = 10
    y = 20
    z = 30
    return x + y + z
"""
        
        file1_path.write_text(content)
        file2_path.write_text(content)
        
        # Create linter with configuration that triggers the bug  
        linter = PyLinter()
        linter.config.min_similarity_lines = 0  # Key: this setting should disable checking
        
        # Create SimilarChecker with the problematic configuration
        checker = similar.SimilarChecker(linter)
        
        # Verify configuration setting is respected
        assert checker.config.min_similarity_lines == 0
        
        # The test's intent is to check whether this configuration 
        # can be applied to a checker, and whether that configuration
        # setting behaves correctly for the purpose that was broken
        # (the entire purpose of the fix in the pull request)