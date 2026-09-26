"""
Regression test for Django issue where generated migration files 
are missing import statements for models.Model when models inherit 
from both a mixin and an abstract model.
"""
from django.db import models
from django.db.migrations.serializer import serializer_factory
from django.test import TestCase


class MyField(models.TextField):
    pass


class MyBaseModel(models.Model):
    class Meta:
        abstract = True


class MyMixin:
    pass


class MigrationWriterTestCase(TestCase):
    def test_type_serializer_includes_models_import_for_model(self):
        """Test that TypeSerializer properly includes 'from django.db import models' 
        when serializing models.Model"""
        
        # Test the serializer directly on models.Model
        serializer = serializer_factory(models.Model)
        result, imports = serializer.serialize()
        
        # This should include the import statement according to the fix
        self.assertIn('from django.db import models', imports)
        self.assertEqual(result, 'models.Model')
        
    def test_type_serializer_includes_models_import_for_bases(self):
        """Test that when serializing bases containing models.Model, 
        the proper import is included"""
        
        # Test serializing bases that include models.Model
        bases = (MyMixin, models.Model)
        serializer = serializer_factory(bases)
        result, imports = serializer.serialize()
        
        # Check that imports includes the models import
        self.assertIn('from django.db import models', imports)
        
        # The result should properly reference models.Model
        self.assertIn('models.Model', result)
        
    def test_exact_bug_scenario(self):
        """Test the exact scenario from the bug report"""
        # This is the exact scenario from the bug report
        # MyModel inherits from both MyMixin and MyBaseModel (which is abstract)
        # When makemigrations runs, it should generate a valid migration file
        
        # Test the serialization that would happen in the migration writer
        # The bases of MyModel would be (MyMixin, models.Model)
        bases = (MyMixin, models.Model)
        serializer = serializer_factory(bases)
        result, imports = serializer.serialize()
        
        # This should include the import to make the generated migration valid
        self.assertIn('from django.db import models', imports)
        self.assertIn('models.Model', result)