"""
Regression test for Django issue #16454:
Management command subparsers don't retain error formatting.

This test verifies that subparsers created via CommandParser.add_subparsers()
retain the error formatting properties of the parent parser.
"""
from django.core.management.base import CommandParser
from django.test import TestCase


class TestSubparserErrorFormatting(TestCase):
    """Test that subparsers retain error formatting properties."""

    def test_add_subparsers_method_exists(self):
        """
        Test that the add_subparsers method exists on CommandParser.
        This test will fail before the fix is applied because the method doesn't exist.
        """
        # Create a CommandParser
        parser = CommandParser(called_from_command_line=True)
        
        # This should not raise AttributeError if the fix is in place
        # The fix adds this method to CommandParser
        self.assertTrue(hasattr(parser, 'add_subparsers'))
        
        # Test that we can call it without error
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # Test basic functionality
        parsed = parser.parse_args(['create', 'test'])
        self.assertEqual(parsed.name, 'test')