"""
Regression test for Django migration import issue - missing import statement.
This validates that when a model inherits from both a mixin and an abstract base class,
migration files correctly include the 'from django.db import models' import.
"""
from django.test import TestCase
from django.db.migrations.serializer import TypeSerializer
from django.db import models


class MigrationImportRegressionTest(TestCase):
    """
    Tests specifically targeting the deleted line that was fixed in the pull request.
    """
    
    def test_serializer_handles_models_model_import_correctly(self):
        """
        Verify the fix for TypeSerializer special_cases handling of models.Model
        
        The fix changed the special_cases entry from:
            (models.Model, "models.Model", []) 
        to:
            (models.Model, "models.Model", ['from django.db import models'])
        
        This test ensures that when models.Model is serialized by TypeSerializer,
        the resulting imports include the proper Django models import statement.
        """
        # This targets the exact code path that was changed in serializer.py line ~276
        serializer = TypeSerializer(models.Model)
        result, imports = serializer.serialize()
        
        # The core assertion: after fix, we should have the import statement
        self.assertEqual(result, "models.Model")
        self.assertIn("from django.db import models", imports)