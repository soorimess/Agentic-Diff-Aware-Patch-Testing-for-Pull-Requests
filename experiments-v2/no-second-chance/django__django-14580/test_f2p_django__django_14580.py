import unittest
from django.db import models
from django.db.migrations.serializer import TypeSerializer


class MigrationWriterRegressionTests(unittest.TestCase):
    """
    Regression test for Django ticket #14580.
    Tests that the TypeSerializer correctly handles models.Model serialization
    to include proper imports.
    """
    
    def test_type_serializer_handles_models_model(self):
        """
        Test that TypeSerializer correctly handles models.Model serialization
        to include 'from django.db import models' import.
        """
        # Create a TypeSerializer for models.Model
        serializer = TypeSerializer(models.Model)
        
        # Serialize it - this should include the import statement
        result, imports = serializer.serialize()
        
        # The result should be "models.Model"
        self.assertEqual(result, "models.Model")
        
        # The imports should include the required import statement
        # This is the core of the bug: it should be ['from django.db import models']
        # but currently returns [] (empty list)
        self.assertIn('from django.db import models', imports)


if __name__ == '__main__':
    unittest.main()