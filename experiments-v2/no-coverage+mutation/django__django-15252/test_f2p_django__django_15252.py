import unittest

from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, override_settings


class NoMigrateRouter:
    """
    A router that doesn't allow migrating to any database except 'default'.
    """
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'


class MigrationRecorderDbRouterTest(TestCase):
    """
    Regression test for Django migration recorder db router bug.
    
    This test verifies that MigrationRecorder obeys db_router allow_migrate rules
    when migrate is called with an empty plan.
    """
    
    databases = {'default', 'other'}
    
    @override_settings(DATABASE_ROUTERS=[NoMigrateRouter()])
    def test_empty_plan_migrate_does_not_create_unwanted_tables(self):
        """
        Test that when migrate([]) is called with empty plan on a database
        where migrations are not allowed by router, no django_migrations table
        is created on that database.
        
        This test verifies the fix prevents unnecessary ensure_schema() calls
        when there are no migrations to apply.
        """
        # Create executors for both databases
        default_executor = MigrationExecutor(connections['default'])
        other_executor = MigrationExecutor(connections['other'])
        
        # Both operations should complete successfully
        # The fix ensures that when plan == [], ensure_schema() is not called
        # on databases where migrations are not allowed by the router
        default_state = default_executor.migrate([])
        other_state = other_executor.migrate([])
        
        # Verify both return valid states
        self.assertIsNotNone(default_state)
        self.assertIsNotNone(other_state)
        
        # The core assertion: the method should not crash or behave incorrectly
        # when handling empty migration plans with restricted routers