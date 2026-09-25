"""
Test for django/django#15252: MigrationRecorder does not obey db_router allow_migrate rules

This regression test ensures that MigrationRecorder.ensure_schema() respects
database router allow_migrate rules and doesn't create the django_migrations table
on databases where migrations are not allowed.
"""
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.test import TestCase, override_settings


class MigrationRouter:
    """Router that only allows migrations on 'default' database."""
    
    def allow_migrate(self, db, app_label, **hints):
        if db == 'default':
            return True
        return False


class TestMigrationRecorderDBRouter(TestCase):
    """Test that MigrationRecorder respects db_router allow_migrate rules."""
    
    databases = {'default', 'other'}
    
    @override_settings(DATABASE_ROUTERS=[MigrationRouter()])
    def test_ensure_schema_respects_router_rules(self):
        """
        MigrationRecorder.ensure_schema() should not create django_migrations table
        on databases where allow_migrate returns False.
        
        This would fail before the fix and pass after the fix.
        """
        # Test with the 'other' database which should not allow migrations
        other_connection = connections['other']
        recorder = MigrationRecorder(other_connection)
        
        # Verify the table doesn't exist initially
        self.assertFalse(recorder.has_table())
        
        # The key test: calling ensure_schema() should not create table on non-migratable db
        # In the buggy version, this would ignore router rules and create the table
        # In the fixed version, this should not create the table 
        recorder.ensure_schema()
        
        # This assertion will fail on buggy code (table gets created)  
        # but should pass on fixed code (table not created)
        self.assertFalse(recorder.has_table(), 
                        "django_migrations table should NOT be created on non-migratable database")