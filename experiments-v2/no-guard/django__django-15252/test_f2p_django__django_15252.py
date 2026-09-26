"""
Regression test for Django issue #15252:
MigrationRecorder does not obey db_router allow_migrate rules
"""
from unittest.mock import patch

from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.test import TestCase, override_settings


class TestRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'


class MigrationRecorderRouterTests(TestCase):
    databases = {'default', 'other'}
    
    def test_ensure_schema_not_called_for_empty_plan_with_blocked_router(self):
        """
        When migrate is called with empty targets and router blocks migrations,
        ensure_schema should not be called to respect router rules.
        """
        with override_settings(DATABASE_ROUTERS=[TestRouter()]):
            with patch.object(MigrationRecorder, 'ensure_schema') as mock_ensure_schema:
                executor = MigrationExecutor(connections['other'])
                executor.migrate([])
                # This assertion will fail on buggy code (where ensure_schema is called)
                # but pass on fixed code (where ensure_schema is not called)
                mock_ensure_schema.assert_not_called()