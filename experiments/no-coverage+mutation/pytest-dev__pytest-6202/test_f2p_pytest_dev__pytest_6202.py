"""
Regression test ensuring that getmodpath() preserves dots before brackets.
"""

import pytest


class TestDotBracketIssue:
    """Class to test specific bracket/dot behavior in test names"""
    
    @pytest.mark.parametrize("param", ["..["])
    def test_foo(self, param):
        """Test that demonstrates the problem with dots + bracket placement"""
        # This will cause reporting to use getmodpath internally
        # The test parameter "..[" should be preserved in final parametrized name
        assert False  # This test exists to check behavior in reporting, not just pass
    
    # The test case that the bug report shows
    # Before fix: displays as "test_boo[.[]" 
    # After fix: displays as "test_boo[..[]"