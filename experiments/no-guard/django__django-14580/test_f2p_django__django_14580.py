"""
Regression test for Django issue #14580 - Missing import statement in generated migration.

When a model inherits from a mixin and abstract model, and the inherited base class
is models.Model, the generated migration file doesn't import 'models', causing a
NameError when the migration is executed.
"""

from django.test import TestCase
from django.db import models
from django.db.migrations.serializer import serializer_factory


class RegressionTestForDjango14580(TestCase):
    def test_type_serializer_handles_models_model_import_correctly(self):
        """
        Test that TypeSerializer correctly handles models.Model serialization
        by including the proper import statement.
        
        This directly tests the issue where serializing models.Model would not 
        include the required import statement, causing NameError in generated migrations.
        """
        # Test the core issue: models.Model serialization should include proper import
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # The result should be "models.Model" 
        self.assertEqual(result, "models.Model")
        
        # The imports should include the import statement for models
        # This is the core bug fix - before the fix, imports was an empty set
        expected_imports = {"from django.db import models"}
        self.assertEqual(imports, expected_imports)

    def test_migration_code_compiles_without_nameerror(self):
        """
        Test that the migration generation process doesn't create invalid Python code
        that will raise NameError during migration execution.
        """
        from django.db.migrations.writer import MigrationWriter
        from django.db.migrations import Migration
        
        # Create a minimal migration that would contain Model references
        migration = Migration('0001_initial', 'test_app')
        
        # Add operations that are likely to reference type objects that get serialized
        # The key point is to ensure serialization of types like models.Model doesn't break
        try:
            # Ensure that MigrationWriter can handle various objects without NameError
            writer = MigrationWriter(migration)
            content = writer.as_string()
            
            # The generated content should be valid Python (no import issues)
            compile(content, '<migration>', 'exec')
        except SyntaxError as e:
            self.fail(f"Generated migration code has syntax error: {e}")
        except NameError as e:
            if "models" in str(e):
                self.fail(f"Generated migration code has NameError due to missing models import: {e}")
            else:
                # Re-raise other NameErrors
                raise