"""
Regression test for Django issue #15252:
MigrationRecorder does not obey db_router allow_migrate rules

This test ensures that when there are no migrations to apply, the MigrationRecorder
does not attempt to create the django_migrations table on databases where
allow_migrate returns False.
"""
from unittest.mock import patch
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class MigrationRecorderRouterTest(TestCase):
    """Test that MigrationRecorder obeys db_router allow_migrate rules."""

    def test_ensure_schema_not_called_with_empty_plan(self):
        """
        Test that ensure_schema is not called when plan is empty.
        This is the core behavior that was fixed in the pull request.
        """
        # Create an executor
        executor = MigrationExecutor(connection)
        
        # Mock the ensure_schema method to track if it's called
        with patch.object(executor.recorder, 'ensure_schema') as mock_ensure_schema:
            # Call migrate with empty plan
            executor.migrate([], plan=[])
            
            # With the fix, ensure_schema should NOT be called when plan is empty
            # Without the fix, ensure_schema would be called
            mock_ensure_schema.assert_not_called()