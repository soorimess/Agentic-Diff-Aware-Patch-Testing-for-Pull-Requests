from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, override_settings


class TestMigrationRecorderDBRouter(TestCase):
    """
    Regression test for the bug where MigrationRecorder does not obey db_router allow_migrate rules.
    
    The fix in executor.py prevents ensure_schema() from being called when there are no 
    migrations to apply, which prevents creating django_migrations table on databases 
    where router disallows migrations.
    """
    
    databases = {'default', 'other'}

    def test_empty_plan_no_table_creation_when_router_blocks(self):
        """
        When there are no migrations to apply (empty plan) and a router
        disallows migrations on 'other' database, ensure_schema() should not be called
        and the django_migrations table should not be created on the 'other' database.
        """
        # Create a router that only allows migrations on 'default' database
        class MigrationRouter:
            def allow_migrate(self, db, app_label, model_name=None, **hints):
                return db == 'default'

        # Set up the router
        with override_settings(DATABASE_ROUTERS=[MigrationRouter()]):
            # Create executors for both databases
            executor_default = MigrationExecutor(connections['default'])
            executor_other = MigrationExecutor(connections['other'])
            
            # Verify initial state - no tables should exist
            self.assertFalse(executor_default.recorder.has_table())
            self.assertFalse(executor_other.recorder.has_table())
            
            # Get migration plan for empty targets - should be empty list
            plan_default = executor_default.migration_plan([])
            plan_other = executor_other.migration_plan([])
            
            # Both should have empty plans (no migrations to apply)
            self.assertEqual(plan_default, [])
            self.assertEqual(plan_other, [])
            
            # Run migrate on both - this is where the fix matters
            # For 'default': should create table normally
            # For 'other': should NOT create table due to router restrictions
            
            # This is the key test - the fix prevents ensure_schema() from being called
            # when plan is empty and there's no existing table
            result_default = executor_default.migrate([])
            result_other = executor_other.migrate([])
            
            # Default should have table (normal behavior)
            self.assertTrue(executor_default.recorder.has_table())
            
            # The fix should prevent table creation on 'other' database
            # This assertion will fail in buggy version (table created) 
            # but pass in fixed version (table not created)
            table_exists_on_other = executor_other.recorder.has_table()
            
            # If table exists on 'other', it means the bug exists
            # The fix should prevent this
            if table_exists_on_other:
                self.fail("django_migrations table was created on 'other' database despite router disallowing migrations")
            
            # If we get here, the fix is working
            self.assertFalse(table_exists_on_other, 
                           "django_migrations table should not be created on 'other' database when router disallows it")