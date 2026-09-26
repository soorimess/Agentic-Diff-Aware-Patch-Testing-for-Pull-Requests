import unittest
from django.db import models
from django.db.migrations.serializer import serializer_factory


class MigrationImportTest(unittest.TestCase):
    """
    Test for Django issue where migration files are missing import statements
    for models.Model when using custom field inheritance.
    This test ensures that TypeSerializer properly includes import statements
    for models.Model, preventing NameError: name 'models' is not defined.
    """
    
    def test_type_serializer_includes_model_import(self):
        """
        Test that TypeSerializer properly includes import statements for models.Model.
        Before the fix, serializing models.Model would return an empty imports set,
        causing generated migrations to have NameError when referencing models.Model.
        """
        # Test the specific case that was failing
        # When models.Model is serialized, it should include the import
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # The result should be "models.Model"
        self.assertEqual(result, "models.Model")
        
        # The key fix: imports should include the import statement for models
        # This was the core bug - before fix it was returning set()
        self.assertIn("from django.db import models", imports)


if __name__ == '__main__':
    unittest.main()