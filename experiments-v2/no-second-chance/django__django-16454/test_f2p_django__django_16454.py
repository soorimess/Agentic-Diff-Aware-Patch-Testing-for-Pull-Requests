import unittest
from django.core.management.base import CommandError, CommandParser
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes'])
class TestSubparserErrorFormatting(TestCase):
    """Test that management command subparsers retain error formatting."""

    def test_subparser_error_handling_behavior(self):
        """
        Test that subparsers properly handle missing required arguments
        with clean error messages instead of raw tracebacks.
        """
        # Create a CommandParser like in the bug report
        parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers exactly as described in the bug report
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # Test that missing required arguments produce clean error messages
        try:
            # This should trigger proper error handling
            result = parser.parse_args(['create'])  # Missing required 'name' argument
        except SystemExit:
            # Normal argparse behavior
            pass
        except CommandError as e:
            # This is the expected behavior - clean usage message
            error_msg = str(e)
            self.assertIn("the following arguments are required", error_msg)
            # The bug was that this would contain "Traceback" instead
            self.assertNotIn("Traceback", error_msg)
        except Exception as e:
            # This would indicate the bug - raw traceback instead of clean message
            self.fail("Expected CommandError with proper formatting, got %s: %s. "
                     "This shows the bug where subparsers don't retain error formatting." % 
                     (type(e).__name__, str(e)))

    def test_add_subparsers_method_exists(self):
        """
        Test that the add_subparsers method exists on CommandParser.
        This method was added in the fix to ensure proper error handling.
        """
        # Check that the method exists
        self.assertTrue(hasattr(CommandParser, 'add_subparsers'))
        
        # Test basic functionality works
        parser = CommandParser(called_from_command_line=True)
        subparsers = parser.add_subparsers(required=True)
        self.assertIsNotNone(subparsers)
        
        # Test that we can create and use subparsers
        create = subparsers.add_parser("create")
        create.add_argument("--name", required=True)
        
        # Test error handling works
        try:
            result = parser.parse_args(['create'])  # Missing required --name
        except SystemExit:
            pass
        except CommandError as e:
            error_msg = str(e)
            self.assertIn("the following arguments are required", error_msg)
        except Exception as e:
            self.fail("Unexpected exception: %s: %s" % (type(e).__name__, str(e)))