"""
Regression test for Django issue #16454:
Management command subparsers don't retain error formatting
"""
from django.test import TestCase
from django.core.management.base import CommandParser
from django.core.management.base import CommandError


class DjangoSubparserErrorFormattingTest(TestCase):
    """
    Tests for Django management command subparser error formatting behavior.
    This test should fail before the fix and pass after the fix.
    """
    
    def test_subparser_inherits_command_line_context(self):
        """
        Test that subparsers created with CommandParser properly inherit
        the called_from_command_line parameter from the parent parser.
        """
        # Create main CommandParser with explicit context
        main_parser = CommandParser(called_from_command_line=True)
        
        # Create subparsers - this action uses the method that was fixed
        subparsers = main_parser.add_subparsers()
        
        # Create a specific subparser 
        subparser = subparsers.add_parser("test_command")
        
        # The fix ensures the subparser gets proper initialization parameters
        self.assertIsInstance(subparser, CommandParser)
        self.assertTrue(hasattr(subparser, 'called_from_command_line'))
        self.assertTrue(subparser.called_from_command_line)
    
    def test_management_command_error_formatting_clean(self):
        """
        Test that command errors produce clean error messages instead of stack traces.
        """
        # Create command structure exactly matching bug report
        main_parser = CommandParser()
        subparsers = main_parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("--name", required=True)
        
        # This should show clean error message, not a traceback
        with self.assertRaises(CommandError) as cm:
            main_parser.parse_args(['create'])
        
        # Ensure it's a clean CommandError, not a traceback
        error_msg = str(cm.exception)
        self.assertNotIn("traceback", error_msg.lower())
        self.assertIn("error:", error_msg.lower())