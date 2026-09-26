import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory


class MigrationGenerationTest(unittest.TestCase):
    def test_type_serializer_for_models_model(self):
        """
        Regression test for Django issue #14580.
        When TypeSerializer encounters models.Model, it should include 
        'from django.db import models' in the imports to avoid NameError
        in generated migration files.
        """
        # Test the specific serializer behavior that was broken
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix: result = "models.Model", imports = set()
        # After the fix: result = "models.Model", imports = {"from django.db import models"}
        
        # The result should contain "models.Model"
        self.assertIn('models.Model', result)
        
        # The imports should include the import statement for models
        # This is the key assertion that will fail before the fix
        self.assertIn('from django.db import models', imports)
        
    def test_type_serializer_for_models_model_returns_correct_result(self):
        """
        Additional test to verify the result string is correct.
        """
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # Verify the result is exactly what we expect for migration generation
        self.assertEqual(result, "models.Model")