# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020-2021 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Maksym Humetskyi <Humetsky@gmail.com>
# Copyright (c) 2021 Aditya Gupta <adityagupta1089@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Tests for the similar checker."""

import os
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch

import pytest

from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import GenericTestReporter as Reporter


def test_min_similarity_lines_zero_returns_early():
    """Test that when min-similarity-lines is 0, run() returns early without computing similarities."""
    # Create two files with similar content
    file1_content = '''def func():
    x = 1
    y = 2
    return x + y

def other_func():
    a = 1
    b = 2
    return a + b
'''

    file2_content = '''def func():
    x = 1
    y = 2
    return x + y

def other_func():
    a = 1
    b = 2
    return a + b
'''

    # Write temporary files
    with open("test_file1.py", "w") as f:
        f.write(file1_content)
    with open("test_file2.py", "w") as f:
        f.write(file2_content)

    try:
        # Test with min_lines = 0 (should return early without computing)
        linter = PyLinter(reporter=Reporter())
        checker = similar.SimilarChecker(linter)
        checker.min_lines = 0  # Set the min_lines to 0
        
        # Add both files to the checker
        with open("test_file1.py", "r") as f:
            checker.append_stream("test_file1.py", f)
        with open("test_file2.py", "r") as f:
            checker.append_stream("test_file2.py", f)
        
        # Mock the _compute_sims and _display_sims methods to see if they're called
        with patch.object(checker, '_compute_sims') as mock_compute, \
             patch.object(checker, '_display_sims') as mock_display:
            
            # Capture output when run is called
            output = StringIO()
            with redirect_stdout(output):
                checker.run()
            
            # When min_lines=0, _compute_sims and _display_sims should NOT be called
            # This is the core of the bug: they ARE being called when they shouldn't be
            assert not mock_compute.called, "_compute_sims should not be called when min_lines=0"
            assert not mock_display.called, "_display_sims should not be called when min_lines=0"
            
    finally:
        # Clean up
        os.unlink("test_file1.py")
        os.unlink("test_file2.py")


def test_min_similarity_lines_positive_computes_similarities():
    """Test that when min-similarity-lines is positive, run() computes similarities."""
    # Create two files with similar content
    file1_content = '''def func():
    x = 1
    y = 2
    return x + y

def other_func():
    a = 1
    b = 2
    return a + b
'''

    file2_content = '''def func():
    x = 1
    y = 2
    return x + y

def other_func():
    a = 1
    b = 2
    return a + b
'''

    # Write temporary files
    with open("test_file3.py", "w") as f:
        f.write(file1_content)
    with open("test_file4.py", "w") as f:
        f.write(file2_content)

    try:
        # Test with min_lines = 3 (should compute similarities)
        linter = PyLinter(reporter=Reporter())
        checker = similar.SimilarChecker(linter)
        checker.min_lines = 3  # Set the min_lines to 3
        
        # Add both files to the checker
        with open("test_file3.py", "r") as f:
            checker.append_stream("test_file3.py", f)
        with open("test_file4.py", "r") as f:
            checker.append_stream("test_file4.py", f)
        
        # Mock the _compute_sims and _display_sims methods to see if they're called
        with patch.object(checker, '_compute_sims') as mock_compute, \
             patch.object(checker, '_display_sims') as mock_display:
            
            # Capture output when run is called
            output = StringIO()
            with redirect_stdout(output):
                checker.run()
            
            # When min_lines>0, _compute_sims and _display_sims SHOULD be called
            assert mock_compute.called, "_compute_sims should be called when min_lines>0"
            assert mock_display.called, "_display_sims should be called when min_lines>0"
            
    finally:
        # Clean up
        os.unlink("test_file3.py")
        os.unlink("test_file4.py")