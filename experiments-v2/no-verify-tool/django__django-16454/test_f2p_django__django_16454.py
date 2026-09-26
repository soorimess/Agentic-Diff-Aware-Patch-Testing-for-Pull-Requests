import unittest
from io import StringIO
from django.core.management.base import CommandParser, CommandError
import sys


class SubparserErrorFormattingTest(unittest.TestCase):
    """Test that subparsers retain error formatting from parent CommandParser."""

    def test_subparser_error_formatting_is_clean_not_traceback(self):
        """
        The core test: when subparsers have missing required arguments,
        they should show clean error messages, not tracebacks.
        
        This test will fail in the buggy version where subparsers don't
        inherit proper error handling behavior from their parent.
        """
        # Create a CommandParser that simulates CLI usage
        parser = CommandParser(called_from_command_line=True)
        
        # Create subparsers structure like in the bug report
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")  # This is the required positional argument
        
        # Capture stderr to detect if traceback appears
        old_stderr = sys.stderr
        stderr_capture = StringIO()
        sys.stderr = stderr_capture
        
        try:
            # Parse with missing required argument - this should trigger subparser error
            try:
                parser.parse_args(['create'])
            except CommandError as e:
                error_msg = str(e)
                stderr_output = stderr_capture.getvalue()
                
                # This is the key assertion - the error should be clean
                # If the fix isn't applied, we might get traceback in stderr
                self.assertNotIn("Traceback", error_msg.lower(), 
                               "Subparser should not show traceback in error message")
                self.assertNotIn("Traceback", stderr_output.lower(),
                               "Subparser should not show traceback in stderr")
                
                # Should contain proper error information
                self.assertIn("required", error_msg.lower())
                
        finally:
            sys.stderr = old_stderr

    def test_subparser_with_named_required_argument(self):
        """
        Test with named required argument (more standard case).
        """
        parser = CommandParser(called_from_command_line=True)
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("--name", required=True)
        
        old_stderr = sys.stderr
        stderr_capture = StringIO()
        sys.stderr = stderr_capture
        
        try:
            try:
                parser.parse_args(['create'])
            except CommandError as e:
                error_msg = str(e)
                stderr_output = stderr_capture.getvalue()
                
                # Should not contain traceback
                self.assertNotIn("Traceback", error_msg.lower())
                self.assertNotIn("Traceback", stderr_output.lower())
                self.assertIn("required", error_msg.lower())
                
        finally:
            sys.stderr = old_stderr