import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory

class MigrationImportTest(unittest.TestCase):
    def test_type_serializer_includes_models_import_for_model_class(self):
        """
        Test that TypeSerializer includes the 'from django.db import models' 
        import when serializing models.Model class itself.
        
        This is a regression test for Django issue where migrations would
        be generated with missing import statements, causing NameError.
        """
        # Test the specific case mentioned in the bug report
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # The bug was that imports was an empty list [] instead of including
        # 'from django.db import models' 
        self.assertIn('from django.db import models', imports,
                    "TypeSerializer should include 'from django.db import models' "
                    "import when serializing models.Model")
        
        # Verify the result is correct
        self.assertEqual(result, "models.Model")