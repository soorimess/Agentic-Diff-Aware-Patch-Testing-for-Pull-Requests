"""
Regression test for Django issue 14580: Missing import statement in generated migration 
(NameError: name 'models' is not defined)

Before the fix, when TypeSerializer serializes models.Model, it returns an empty imports 
set instead of including 'from django.db import models', causing generated migration files 
to have NameError when executing.
"""
from django.test import SimpleTestCase
from django.db.migrations.serializer import serializer_factory
from django.db import models


class MigrationSerializerRegressionTest(SimpleTestCase):
    def test_type_serializer_includes_models_import_for_model(self):
        """
        Test that TypeSerializer for models.Model correctly includes the required import.
        
        Before fix: imports = set() (empty) 
        After fix:  imports = {'from django.db import models'}
        """
        # Test the specific issue reported
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # The fix ensures this import is present
        self.assertIn('from django.db import models', imports)
        self.assertEqual(result, 'models.Model')