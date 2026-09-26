# Copyright (c) 2023, 2024 PyCQA and contributors
# SPDX-License-Identifier: GPL-2.0-or-later

"""Regression test for issue where min-similarity-lines=0 should disable duplicate code checking."""

import tempfile
import os
from io import StringIO
from contextlib import redirect_stdout
from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter


def test_min_similarity_lines_zero_no_processing():
    """Test that when min-similarity-lines=0, _compute_sims is not called."""
    
    # Create test files with content that would trigger duplicate detection
    file1_content = '''def func():
    x = 1
    y = 2
    return x + y
'''
    
    file2_content = '''def func():
    x = 1
    y = 2
    return x + y
'''
    
    # Write test files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1:
        f1.write(file1_content)
        file1_path = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
        f2.write(file2_content)
        file2_path = f2.name
    
    try:
        # Test with min_similarity_lines = 0
        linter = PyLinter(reporter=Reporter())
        checker = similar.SimilarChecker(linter)
        checker.min_lines = 0
        
        # Monkey patch to detect if _compute_sims is called
        import pylint.checkers.similar as similar_module
        
        # Store original method
        original_compute_sims = similar_module.SimilarChecker._compute_sims
        
        compute_sims_called = [False]  # Use list to make it mutable in closure
        
        def mock_compute_sims(self):
            compute_sims_called[0] = True
            return []
        
        # Replace the method with our mock
        similar_module.SimilarChecker._compute_sims = mock_compute_sims
        
        # Append streams to the checker
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            checker.append_stream('file1', f1)
            checker.append_stream('file2', f2)
        
        # Run the checker
        checker.run()
        
        # If the fix is in place, _compute_sims should NOT be called
        # If the bug exists, _compute_sims would be called
        assert not compute_sims_called[0], "When min_lines=0, _compute_sims should not be called"
        
    finally:
        # Restore original method
        similar_module.SimilarChecker._compute_sims = original_compute_sims
        # Clean up temp files
        os.unlink(file1_path)
        os.unlink(file2_path)