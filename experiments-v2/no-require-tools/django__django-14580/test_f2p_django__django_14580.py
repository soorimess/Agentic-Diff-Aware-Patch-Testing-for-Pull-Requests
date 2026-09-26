import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory


class SerializerRegressionTest(unittest.TestCase):
    """Test serializer behavior for models.Model references."""
    
    def test_type_serializer_includes_models_import_for_model_reference(self):
        """
        Regression test for Django #14580.
        Tests that TypeSerializer properly includes import statements for models.Model references
        in migration files to prevent NameError: name 'models' is not defined.
        """
        # Test the specific case that was broken: serializing models.Model
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix: result="models.Model", imports=set()
        # After the fix: result="models.Model", imports={"from django.db import models"}
        self.assertEqual(result, "models.Model")
        self.assertIn("from django.db import models", imports)
        
        # Verify it's the right import - not just any import
        self.assertEqual(len(imports), 1)
        self.assertEqual(list(imports)[0], "from django.db import models")