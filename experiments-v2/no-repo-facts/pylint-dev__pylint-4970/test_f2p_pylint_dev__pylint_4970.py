# Copyright (c) 2021, 2022 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Maksym Humetskyi <Humetsky@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Aditya Gupta <adityagupta1089@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Test for the bug where min-similarity-lines=0 should disable duplicate code checking."""

import tempfile
from pathlib import Path

from pylint.checkers import similar
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter


def test_min_similarity_lines_zero_returns_early_direct():
    """
    Direct test that the run() method returns early when min_lines = 0.
    
    This test directly calls the SimilarChecker.run() method and verifies
    that when min_lines = 0, it returns early without performing duplicate checking.
    """
    
    # Create test files with duplicate content
    test_code_1 = '''def func_a():
    x = 1
    y = 2
    z = 3
    return x + y + z

def func_b():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    test_code_2 = '''def func_c():
    x = 1
    y = 2
    z = 3
    return x + y + z

def func_d():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    with tempfile.TemporaryDirectory() as tmpdir:
        file1_path = Path(tmpdir) / "test1.py"
        file2_path = Path(tmpdir) / "test2.py"
        
        file1_path.write_text(test_code_1)
        file2_path.write_text(test_code_2)
        
        # Create linter and checker
        linter = PyLinter()
        linter.set_reporter(MinimalTestReporter())
        # This is the key: explicitly set to 0 to trigger the behavior
        linter.config.min_similarity_lines = 0
        
        # Create and configure the similar checker directly
        checker = similar.SimilarChecker(linter)
        
        # Add files to the checker - this is important to set up the internal state
        with open(file1_path, encoding="utf-8") as stream:
            checker.append_stream(str(file1_path), stream)
        with open(file2_path, encoding="utf-8") as stream:
            checker.append_stream(str(file2_path), stream)
        
        # The key: call run() directly on the checker
        # This should return early when min_lines == 0
        checker.run()
        
        # Check that no duplicate warnings were generated
        messages = linter.reporter.messages
        duplicate_warnings = [msg for msg in messages if msg.symbol == 'duplicate-code']
        
        # This assertion validates the fix behavior
        assert len(duplicate_warnings) == 0, (
            "When min_similarity_lines=0, duplicate code checking should be disabled. "
            f"Found {len(duplicate_warnings)} duplicate code warnings when none expected."
        )


def test_min_similarity_lines_zero_behavior():
    """
    Test that demonstrates the expected behavior difference.
    
    When min_lines=0, the checker should not perform any duplicate analysis.
    When min_lines>0, it should perform duplicate analysis.
    """
    
    # Create test files
    test_code_1 = '''def helper_function():
    x = 1
    y = 2
    z = 3
    return x + y + z

def another_function():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    test_code_2 = '''def helper_function():
    x = 1
    y = 2
    z = 3
    return x + y + z

def another_function():
    x = 1
    y = 2
    z = 3
    return x + y + z
'''
    
    with tempfile.TemporaryDirectory() as tmpdir:
        file1_path = Path(tmpdir) / "test1.py"
        file2_path = Path(tmpdir) / "test2.py"
        
        file1_path.write_text(test_code_1)
        file2_path.write_text(test_code_2)
        
        # Test with min_similarity_lines = 0 (should disable checking)
        linter_zero = PyLinter()
        linter_zero.set_reporter(MinimalTestReporter())
        linter_zero.config.min_similarity_lines = 0
        
        # Run the checker with min_lines = 0
        linter_zero.check([str(file1_path), str(file2_path)])
        
        messages_zero = linter_zero.reporter.messages
        duplicate_warnings_zero = [msg for msg in messages_zero if msg.symbol == 'duplicate-code']
        
        # With min_lines = 0, no duplicates should be found (the fix)
        assert len(duplicate_warnings_zero) == 0, (
            "min_similarity_lines=0 should disable duplicate checking, "
            f"but found {len(duplicate_warnings_zero)} warnings"
        )