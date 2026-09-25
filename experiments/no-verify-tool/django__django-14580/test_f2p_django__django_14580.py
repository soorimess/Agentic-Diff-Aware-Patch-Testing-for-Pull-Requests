"""
Regression test for Django bug #14580 - Missing import statement in generated migration.
"""

from django.test import SimpleTestCase
from django.db import models


class MigrationImportRegressionTest(SimpleTestCase):
    
    def test_models_model_serialization_imports(self):
        """
        Test that type serialization of models.Model properly includes import statements.
        The bug was that when models.Model appears in migrations (like in bases parameter),
        the generated migration file is missing the import statement for 'from django.db import models',
        causing a NameError when the migration is run.
        """
        # Test the core problem that causes the bug
        from django.db.migrations.serializer import TypeSerializer
        
        # This is the specific case from the diff in the bug report
        ts = TypeSerializer(models.Model)
        result, imports = ts.serialize()
        
        # The bug: imports was empty set() instead of containing the import
        # Expected behavior after fix: should include import statement
        self.assertIn('from django.db import models', imports,
                     "models.Model serialization should include proper import statement "
                     "to avoid NameError in generated migrations")
        
        # Also verify that the result string is correct
        self.assertEqual(result, "models.Model")