"""
Regression test for Django issue #14580
Test that migration files properly import 'models' when generating 
code with bases that include models.Model.
"""

import sys
import os
from django.test import TestCase


class TestMigrationSerialization(TestCase):
    def test_type_serializer_includes_models_import_for_model(self):
        """
        Test that TypeSerializer properly includes 'from django.db import models' 
        when serializing models.Model to ensure generated migration files are valid Python.
        """
        # Import after Django setup to make sure modules are available
        from django.db.migrations.serializer import TypeSerializer
        from django.db import models
        
        # Create a TypeSerializer for models.Model
        serializer = TypeSerializer(models.Model)
        result, imports = serializer.serialize()
        
        # Before the fix: result = "models.Model", imports = set()
        # After the fix: result = "models.Model", imports = {'from django.db import models'}
        expected_import = 'from django.db import models'
        
        # Check that the proper import is included 
        self.assertIn(expected_import, imports)
        
        # Also check that the result string is correct
        self.assertEqual(result, "models.Model")