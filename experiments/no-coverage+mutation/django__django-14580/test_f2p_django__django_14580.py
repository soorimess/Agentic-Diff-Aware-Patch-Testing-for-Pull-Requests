"""
Regression test for Django migrations serializer bug.
This pins down the exact behavior that was broken and fixed.
"""
from django.test import SimpleTestCase


class MigrationSerializerRegressionTest(SimpleTestCase):
    def test_type_serializer_includes_models_import_for_model(self):
        """
        Test that TypeSerializer correctly handles models.Model by including
        the required import statement.
        
        Before fix: TypeSerializer.serialize() with models.Model returned 
        ("models.Model", set()) - no imports
        After fix: TypeSerializer.serialize() with models.Model should return
        ("models.Model", {"from django.db import models"}) - with correct import
        
        This was causing NameError when generated migrations referenced models.Model
        without importing 'from django.db import models'.
        """
        from django.db.migrations.serializer import TypeSerializer
        from django.db import models
        
        # The core test: TypeSerializer for models.Model should include proper import
        serializer = TypeSerializer(models.Model)
        result_string, result_imports = serializer.serialize()
        
        # These are the two behaviors that must be correct:
        self.assertEqual(result_string, "models.Model")
        self.assertIn("from django.db import models", result_imports)