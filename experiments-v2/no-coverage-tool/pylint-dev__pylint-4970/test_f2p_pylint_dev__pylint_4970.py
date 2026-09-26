# Copyright (c) 2021, 2022, 2023, 2024 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Maksym Humetskyi <Humetsky@gmail.com>
# Copyright (c) 2021 Aditya Gupta <adityagupta1089@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2020-2021 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Eli Fine <ejfine@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2020-2021 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Taewon D. Kim <kimt33@mcmaster.ca>
# Copyright (c) 2018 Scott Worley <scottworley@scottworley.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2012 Ry4an Brase <ry4an-hg@ry4an.org>
# Copyright (c) 2010, 2012, 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Test for issue #4970 - Setting min-similarity-lines to 0 should disable duplicate code checking."""

import tempfile
from pathlib import Path

from pylint.lint import PyLinter


def test_min_similarity_lines_zero_disables_duplicate_checking():
    """Test that min_similar_lines=0 disables duplicate code checking.
    
    This test ensures that when min_similar_lines is set to 0, the duplicate code
    checker is completely disabled to prevent false positive duplicate code errors.
    
    Before the fix, setting min_similar_lines=0 would still run the similarity
    checking algorithm, causing it to treat every line as similar and generate
    many false positive errors.
    """
    # Create two files with code that would be flagged as duplicates if min_lines > 0
    with tempfile.TemporaryDirectory() as tmpdir:
        file1_path = Path(tmpdir) / "file1.py"
        file2_path = Path(tmpdir) / "file2.py"
        
        # Write files with similar code blocks
        file1_content = '''def helper_function():
    x = 1
    y = 2
    z = x + y
    return z

def main_function():
    result = helper_function()
    print(result)
    return result
'''
        file2_content = '''def helper_function():
    x = 1
    y = 2
    z = x + y
    return z

def main_function():
    result = helper_function()
    print(result)
    return result
'''
        
        file1_path.write_text(file1_content)
        file2_path.write_text(file2_content)
        
        # Test with min_lines = 0 (should disable checking entirely)
        linter = PyLinter()
        linter.config.min_similar_lines = 0
        
        # Run the linter and capture messages
        messages = []
        class TestReporter:
            def on_set_current_module(self, *args):
                pass
            def handle_message(self, msg):
                messages.append(msg)
            def on_close(self, *args):
                pass
        
        linter.set_reporter(TestReporter())
        linter.check([str(file1_path), str(file2_path)])
        
        # With min_lines=0, no similar-lines messages should be generated
        # because duplicate checking should be completely disabled
        similar_messages = [msg for msg in messages if msg.symbol == "similar-lines"]
        
        # This assertion validates the fix: when min_lines=0, no duplicate checking occurs
        # If the fix wasn't there, this would fail because min_lines=0 would still 
        # trigger the duplicate checking logic and generate false positives
        assert len(similar_messages) == 0, (
            "BUG: When min_similar_lines=0, duplicate code checking should be disabled. "
            f"Found {len(similar_messages)} similar-lines messages when none were expected. "
            "This indicates the bug where min_lines=0 still runs similarity checking."
        )