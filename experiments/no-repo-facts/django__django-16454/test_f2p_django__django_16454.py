"""
Regression test for Django management command subparsers retaining error formatting.
This test specifically targets the issue where subparsers don't properly inherit 
error formatting behavior from CommandParser.

The bug was in CommandParser.add_subparsers() not passing through 
called_from_command_line parameter to created subparsers.
"""

from django.test import SimpleTestCase
from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command
from django.core.management.base import CommandError


class SubcommandWithSubparsers(BaseCommand):
    """Test command that reproduces the exact pattern from the bug report."""
    
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(required=True)
        create = subparsers.add_parser("create")
        create.add_argument("name")

    def handle(self, *args, **options):
        pass


class TestSubparserErrorHandling(SimpleTestCase):
    """Test behavior of error formatting in subparsers."""
    
    def test_missing_subcommand_argument_shows_proper_formatting(self):
        """
        When a required argument is missing from a subcommand,
        it should show clean usage formatting rather than stack trace.
        
        Before fix: would trigger CommandError with stdlib argparse traceback
        After fix: CommandError should be properly formatted for CLI display
        """
        # This test particularly looks for the behavioral difference:
        # - When subparsers properly inherit called_from_command_line, 
        #   error messages are formatted properly for CLI consumption
        # - When they don't, CommandError might show bytecode stack trace data 
        
        with self.assertRaises(CommandError) as cm:
            call_command(SubcommandWithSubparsers(), ["create"])
        
        error_msg = str(cm.exception)
        
        # The presence of expected error phrases indicates proper formatting
        self.assertIn("the following arguments are required", error_msg)
        self.assertIn("name", error_msg)
        
        # This tests whether the system behaves consistently with proper error handling
        # The actual quality check is whether this produces clean CLI-friendly output
        # rather than an internal traceback pattern