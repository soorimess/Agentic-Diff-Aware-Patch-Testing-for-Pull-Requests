"""
Regression test for database collation support in CharField and TextField.
This test ensures that CharField and TextField can accept a db_collation parameter
and that it's properly handled by the database backends.
"""
import unittest
from django.db import models
from django.test import TestCase


class CollationFieldTest(TestCase):
    def test_charfield_db_collation_parameter(self):
        """Test that CharField accepts db_collation parameter."""
        # This should not raise an error
        field = models.CharField(max_length=100, db_collation='utf8_general_ci')
        self.assertEqual(field.db_collation, 'utf8_general_ci')

    def test_textfield_db_collation_parameter(self):
        """Test that TextField accepts db_collation parameter."""
        # This should not raise an error
        field = models.TextField(db_collation='utf8_general_ci')
        self.assertEqual(field.db_collation, 'utf8_general_ci')

    def test_charfield_db_collation_none(self):
        """Test that CharField works normally when db_collation is None."""
        field = models.CharField(max_length=100)
        self.assertIsNone(field.db_collation)

    def test_textfield_db_collation_none(self):
        """Test that TextField works normally when db_collation is None."""
        field = models.TextField()
        self.assertIsNone(field.db_collation)

    def test_charfield_deconstruct(self):
        """Test that CharField deconstruct method includes db_collation."""
        field = models.CharField(max_length=100, db_collation='utf8_general_ci')
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('db_collation', kwargs)
        self.assertEqual(kwargs['db_collation'], 'utf8_general_ci')

    def test_textfield_deconstruct(self):
        """Test that TextField deconstruct method includes db_collation."""
        field = models.TextField(db_collation='utf8_general_ci')
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('db_collation', kwargs)
        self.assertEqual(kwargs['db_collation'], 'utf8_general_ci')

    def test_charfield_deconstruct_no_collation(self):
        """Test that CharField deconstruct method doesn't include db_collation when None."""
        field = models.CharField(max_length=100)
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('db_collation', kwargs)

    def test_textfield_deconstruct_no_collation(self):
        """Test that TextField deconstruct method doesn't include db_collation when None."""
        field = models.TextField()
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('db_collation', kwargs)

    def test_field_has_db_collation_attribute(self):
        """Test that fields have the db_collation attribute set correctly."""
        char_field = models.CharField(max_length=100, db_collation='utf8_general_ci')
        text_field = models.TextField(db_collation='utf8_general_ci')
        
        # Verify the attributes exist and are set correctly
        self.assertTrue(hasattr(char_field, 'db_collation'))
        self.assertTrue(hasattr(text_field, 'db_collation'))
        self.assertEqual(char_field.db_collation, 'utf8_general_ci')
        self.assertEqual(text_field.db_collation, 'utf8_general_ci')
        
        # Test with None value
        char_field_none = models.CharField(max_length=100)
        text_field_none = models.TextField()
        self.assertIsNone(char_field_none.db_collation)
        self.assertIsNone(text_field_none.db_collation)

    def test_database_features_collation_support(self):
        """Test that database features have the collation support attributes."""
        # Test that the base features class has the expected attributes
        from django.db.backends.base.features import BaseDatabaseFeatures
        features = BaseDatabaseFeatures(None)
        
        # These should exist and be set to expected default values
        self.assertTrue(hasattr(features, 'supports_collation_on_charfield'))
        self.assertTrue(hasattr(features, 'supports_collation_on_textfield'))
        self.assertTrue(hasattr(features, 'supports_non_deterministic_collations'))
        
        # Check that they have the correct default values (True for base class)
        self.assertTrue(features.supports_collation_on_charfield)
        self.assertTrue(features.supports_collation_on_textfield)
        self.assertTrue(features.supports_non_deterministic_collations)