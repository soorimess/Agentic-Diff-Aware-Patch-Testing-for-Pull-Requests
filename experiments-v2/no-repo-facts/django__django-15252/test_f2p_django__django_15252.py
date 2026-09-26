"""
Test for Django issue #15252: MigrationRecorder does not obey db_router allow_migrate rules

This test verifies that when there are no migrations to apply, the MigrationRecorder
should not create the django_migrations table on databases where migrations are not
allowed by the router.
"""
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, override_settings


class MigrationRouter:
    """Router that only allows migrations on the 'default' database."""
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'


class MigrationRecorderRouterTest(TestCase):
    """Test MigrationRecorder behavior with database routers."""
    
    databases = {'default', 'other'}
    
    def test_empty_plan_no_table_creation_on_other_db(self):
        """
        When there are no migrations to apply (empty plan), 
        the django_migrations table should not be created on databases
        where migrations are not allowed by the router.
        
        This test verifies the fix for Django issue #15252 where 
        MigrationRecorder.ensure_schema() was called even when there were
        no migrations to apply, causing tables to be created on databases
        where migrations are not allowed by the router.
        """
        # Setup router that prevents migrations on 'other' database
        router = MigrationRouter()
        
        # Test with empty plan - no migrations to apply
        # In the buggy version, ensure_schema() would be called and try to create table
        # In the fixed version, it should return early without calling ensure_schema()
        with override_settings(DATABASE_ROUTERS=[router]):
            # Create executor for 'other' database (where migrations are NOT allowed)
            executor = MigrationExecutor(connections['other'])
            
            # Check that django_migrations table doesn't exist yet
            self.assertFalse(
                executor.recorder.has_table(), 
                "django_migrations table should not exist initially"
            )
            
            # Run migrate with empty plan - this should not create the table
            # on databases where migrations are not allowed by the router
            result = executor.migrate([], plan=[])
            
            # The key assertion: the table should not be created because:
            # 1. There are no migrations to apply (empty plan)  
            # 2. The router prevents migrations on 'other' database
            # 3. With the fix, ensure_schema() should not be called
            self.assertFalse(
                executor.recorder.has_table(),
                "django_migrations table should not be created on 'other' database when no migrations to apply"
            )