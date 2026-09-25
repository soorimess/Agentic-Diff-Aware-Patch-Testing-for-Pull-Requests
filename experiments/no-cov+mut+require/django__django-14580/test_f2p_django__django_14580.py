"""
Regression test for Django issue where migrations with model inheritance
from models.Model directly don't include proper imports, causing NameError.
"""
from django.db import models
from django.db.migrations.serializer import serializer_factory
from django.test import SimpleTestCase


class MigrationWriterRegressionTest(SimpleTestCase):
    """Test for the migration writer bug with model inheritance imports."""

    def test_serializer_includes_models_import_for_models_model(self):
        """
        Test that serializing models.Model includes the import statement
        to prevent NameError in generated migrations.
        
        Before the fix: serializer_factory(models.Model) returns ("models.Model", set())
        After the fix: serializer_factory(models.Model) returns ("models.Model", {"from django.db import models"})
        """
        # This directly tests the core issue in the bug report
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # The serialized value should be "models.Model"
        self.assertEqual(result, "models.Model")
        
        # The critical test: this import statement should be included
        # to prevent NameError in generated migration files
        self.assertIn("from django.db import models", imports)