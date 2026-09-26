import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory


class RegressionTest(unittest.TestCase):
    def test_type_serializer_handles_models_model_import(self):
        """
        Test that TypeSerializer properly includes import for models.Model.
        This test ensures that when models.Model is serialized, it includes
        the necessary import statement to avoid NameError in generated migrations.
        """
        # Test the specific case that was broken
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix, this would return "models.Model" with empty imports
        # After the fix, this should return "models.Model" with imports including "from django.db import models"
        self.assertEqual(result, "models.Model")
        self.assertIn("from django.db import models", imports)