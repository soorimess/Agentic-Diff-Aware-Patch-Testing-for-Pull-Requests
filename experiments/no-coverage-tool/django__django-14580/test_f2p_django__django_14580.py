"""
Regression test for Django issue #14580: Missing import statement in generated migration.
This test verifies that when models.Model is serialized in migrations, the appropriate
import statement 'from django.db import models' is included.
"""
from django.test import TestCase
from django.db.migrations.serializer import serializer_factory
from django.db import models


class MigrationImportRegressionTest(TestCase):
    def test_models_model_import_in_serializer(self):
        """
        Test that TypeSerializer properly generates import for models.Model.
        
        Before the fix: imports was an empty set
        After the fix: imports should include 'from django.db import models'
        """
        serializer = serializer_factory(models.Model)
        value, imports = serializer.serialize()
        
        # The issue was that without the fix, this would be an empty set
        # When fixed, it should include the import statement
        self.assertIn('from django.db import models', imports)
        
    def test_models_model_serialized_value(self):
        """
        Test that the serialized value for models.Model is correct.
        """
        serializer = serializer_factory(models.Model)
        value, imports = serializer.serialize()
        
        # The value itself should be 'models.Model' 
        self.assertEqual(value, "models.Model")
        
    def test_migration_creation_scenario(self):
        """
        Test the actual scenario from the bug report:
        A model inherits from both a mixin and an abstract model, which should 
        generate a bases tuple like (mixin, models.Model) and require the import.
        """
        # Directly test the code path that would have the problem
        from django.db.migrations.serializer import TypeSerializer
        
        # This is the core test - the TypeSerializer should add imports for models.Model
        type_serializer = TypeSerializer(models.Model)
        value, imports = type_serializer.serialize()
        
        # Verify the imports and value are generated correctly
        self.assertEqual(value, "models.Model")
        self.assertIn('from django.db import models', imports)