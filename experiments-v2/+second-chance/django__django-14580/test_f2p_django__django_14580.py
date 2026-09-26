import unittest
from django.conf import settings
from django.db import models
from django.db.migrations.serializer import TypeSerializer
from django.test import SimpleTestCase


class RegressionTest(SimpleTestCase):
    def test_serializer_handles_models_model_special_case(self):
        """
        Test that the TypeSerializer properly handles models.Model serialization
        by including the necessary import statement.
        
        This is a regression test for Django issue #14580 where the generated migration
        would have a NameError because 'models' was not imported in the generated file.
        """
        # Test the specific case that was broken - models.Model serialization
        serializer = TypeSerializer(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix, this would return "models.Model" with empty imports set()
        # After the fix, this should return "models.Model" with imports including 'from django.db import models'
        
        # The key test: the imports should contain the import statement for models
        # This is what was missing and caused the NameError in migration files
        self.assertIn('from django.db import models', imports, 
                    "models.Model serialization should include import statement for models")
        
        # The serialized value should be "models.Model"
        self.assertEqual(result, "models.Model")
        
    def test_serializer_handles_models_model_special_case_with_imports(self):
        """
        More detailed test to verify the exact behavior change.
        """
        # Test that we get the right imports for models.Model
        serializer = TypeSerializer(models.Model)
        result, imports = serializer.serialize()
        
        # Before fix: imports would be set()
        # After fix: imports should be {'from django.db import models'}
        expected_imports = {'from django.db import models'}
        
        # Check that we have the expected import
        self.assertEqual(imports, expected_imports)