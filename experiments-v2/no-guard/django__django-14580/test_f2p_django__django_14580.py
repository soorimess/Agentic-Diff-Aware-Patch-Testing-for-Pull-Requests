import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory
from django.test import SimpleTestCase


class MigrationWriterRegressionTest(SimpleTestCase):
    """
    Regression test for Django issue #14580: Missing import statement in generated migration
    """
    
    def test_type_serializer_handles_models_model_special_case(self):
        """
        Test that TypeSerializer properly handles models.Model special case
        by including the required import statement.
        """
        # Create a serializer for models.Model
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix, this would return "models.Model" with empty imports []
        # After the fix, this should return "models.Model" with imports {'from django.db import models'}
        self.assertEqual(result, "models.Model")
        
        # This is the key assertion - the import should be included
        self.assertIn("from django.db import models", imports)