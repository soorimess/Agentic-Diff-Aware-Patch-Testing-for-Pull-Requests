from django.test import TestCase
from django.db import models
from django.db.migrations.serializer import serializer_factory


class MigrationSerializerRegressionTest(TestCase):
    """
    Regression test for Django issue where migration serializer doesn't include
    proper imports for models.Model when serializing type objects.
    This test specifically addresses the bug reported in Django issue 14580.
    """
    
    def test_type_serializer_includes_models_import_for_model_class(self):
        """
        Test that when serializing models.Model, the serializer includes
        the proper import statement 'from django.db import models'.
        """
        # Create a serializer for models.Model
        serializer = serializer_factory(models.Model)
        result_string, imports = serializer.serialize()
        
        # The result should be "models.Model"
        self.assertEqual(result_string, "models.Model")
        
        # The imports should include the django.db import - this is the core fix
        expected_imports = {'from django.db import models'}
        self.assertEqual(imports, expected_imports)