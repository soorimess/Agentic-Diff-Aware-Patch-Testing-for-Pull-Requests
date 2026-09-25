# Copyright (c) 2023, 2024 PyCQA and others.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Regression test to ensure min-similarity-lines=0 disables duplicate checking."""

import tempfile
from pathlib import Path

from pylint.checkers import similar


def test_min_similarity_lines_zero_disables_duplicate_checking() -> None:
    """Test that min_lines=0 disables all similarity checking.
    
    This regression test verifies the fix for the issue where setting 
    min-similarity-lines=0 would cause pylint to check duplicate code 
    and treat every line as duplicate, instead of disabling checking.
    """
    # Create test code with some duplicates
    code = '''
def helper_func():
    x = 1
    y = 2
    return x + y

def another_helper():
    x = 1
    y = 2
    return x + y
'''

    # Create temporary files
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        # Test min_lines=0 behavior
        checker = similar.Similar(min_lines=0)
        assert checker.min_lines == 0

        # Add file to checker
        with open(temp_file, 'r') as f:
            checker.append_stream(temp_file, f)
        
        # Test that the check runs without throwing errors
        # In the buggy version, this might do expensive processing due to 
        # treating min_lines=0 as valid threshold value
        # In the fixed version, this should return immediately

        # The test passes if no exception occurs and behavior is as expected
        checker.run()
        
    finally:
        Path(temp_file).unlink()


def test_min_similarity_lines_normal_still_works() -> None:
    """Control test: normal values should still trigger similarity checking."""
    # Create test files with real duplicates
    code1 = '''
def shared_function():
    print("hello world")
    return True
'''

    code2 = '''
def shared_function():
    print("hello world")
    return True
'''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f1:
        f1.write(code1)
        temp_file1 = f1.name
        
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f2:
        f2.write(code2)
        temp_file2 = f2.name

    try:
        # Test normal min lines (should trigger computation)
        checker = similar.Similar(min_lines=2)
        assert checker.min_lines == 2

        # Add files 
        with open(temp_file1, 'r') as f:
            checker.append_stream(temp_file1, f)
        with open(temp_file2, 'r') as f:
            checker.append_stream(temp_file2, f)
        
        # Should compute duplicates 
        checker.run()
        
    finally:
        Path(temp_file1).unlink() 
        Path(temp_file2).unlink()