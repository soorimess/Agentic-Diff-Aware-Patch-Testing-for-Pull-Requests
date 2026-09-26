"""
Test for Django management command subparsers retaining error formatting.

This test verifies that subparsers created by CommandParser retain the error
formatting improvements that are available on the parent parser.
"""
import sys
from io import StringIO
from unittest import TestCase

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.test import TestCase as DjangoTestCase


class TestSubparserErrorFormatting(DjangoTestCase):
    """Test that subparsers retain error formatting from CommandParser."""

    def test_subparser_missing_required_argument_shows_usage(self):
        """
        Test that when a required argument is missing from a subparser,
        it shows a human-readable usage message instead of a stack trace.
        """
        # Create a command that uses subparsers
        class TestCommand(BaseCommand):
            help = "Test command with subparsers"
            
            def add_arguments(self, parser):
                subparsers = parser.add_subparsers(required=True)
                create = subparsers.add_parser("create")
                create.add_argument("name")
                create.add_argument("--verbose", action="store_true")
                
            def handle(self, *args, **options):
                return "success"
        
        # We'll test the behavior by capturing stderr and checking if it's a clean error
        # rather than a stack trace. This requires creating a proper command
        # and testing it through the management command system.
        
        # For now, let's test the core functionality by directly testing the parser
        from django.core.management.base import CommandParser
        
        # Create a parser instance
        parser = CommandParser(called_from_command_line=True)
        
        # Add subparsers like in the bug report
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")
        
        # Test that the subparser has the right attributes
        # This is the core of the issue - subparsers should inherit the called_from_command_line
        # attribute from the parent parser
        
        # Try to parse arguments that should fail
        try:
            # This should fail with a clean error, not a stack trace
            parser.parse_args(['create'])
        except SystemExit:
            # This is expected - the parser exits when arguments are missing
            # The key is that it should exit cleanly with a proper error message
            pass
        except Exception as e:
            # If we get a different exception (like a stack trace), the bug exists
            self.fail(f"Unexpected exception type: {type(e).__name__}: {e}")